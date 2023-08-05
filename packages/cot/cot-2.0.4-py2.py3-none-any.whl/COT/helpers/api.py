#!/usr/bin/env python
#
# api.py - API to abstract away operations that require third-party
#          helper software not part of a standard Python distro.
#
# April 2014, Glenn F. Matthews
# Copyright (c) 2013-2016 the COT project developers.
# See the COPYRIGHT.txt file at the top-level directory of this distribution
# and at https://github.com/glennmatthews/cot/blob/master/COPYRIGHT.txt.
#
# This file is part of the Common OVF Tool (COT) project.
# It is subject to the license terms in the LICENSE.txt file found in the
# top-level directory of this distribution and at
# https://github.com/glennmatthews/cot/blob/master/LICENSE.txt. No part
# of COT, including this file, may be copied, modified, propagated, or
# distributed except according to the terms contained in the LICENSE.txt file.

"""API for abstract access to third-party helper tools.

Abstracts away operations that require third-party helper programs,
especially those that are not available through PyPI.

The actual helper programs are provided by individual classes in this package.

**Functions**

.. autosummary::
  :nosignatures:

  convert_disk_image
  create_disk_image
  create_install_dir
  download_and_expand
  get_checksum
  get_disk_capacity
  get_disk_format
  install_file
"""

import contextlib
import hashlib
import logging
import os
import re
import shutil
import tarfile

from distutils.version import StrictVersion
import requests

from .helper import Helper, guess_file_format_from_path
from .fatdisk import FatDisk
from .mkisofs import MkIsoFS
from .ovftool import OVFTool
from .qemu_img import QEMUImg
from .vmdktool import VmdkTool

logger = logging.getLogger(__name__)

FATDISK = FatDisk()
MKISOFS = MkIsoFS()
OVFTOOL = OVFTool()
QEMUIMG = QEMUImg()
VMDKTOOL = VmdkTool()

BLOCKSIZE = 65536

try:
    # Python 3.x
    from tempfile import TemporaryDirectory
except ImportError:
    # Python 2.x
    import tempfile

    @contextlib.contextmanager
    def TemporaryDirectory(suffix='',   # noqa: N802
                           prefix='tmp',
                           dirpath=None):
        """Create a temporary directory and make sure it's deleted later.

        Reimplementation of Python 3's ``tempfile.TemporaryDirectory``.
        """
        tempdir = tempfile.mkdtemp(suffix, prefix, dirpath)
        try:
            yield tempdir
        finally:
            shutil.rmtree(tempdir)


@contextlib.contextmanager
def download_and_expand(url):
    """Context manager for downloading and expanding a .tar.gz file.

    Creates a temporary directory, downloads the specified URL into
    the directory, unzips and untars the file into this directory,
    then yields to the given block. When the block exits, the temporary
    directory and its contents are deleted.

    ::

      with download_and_expand("http://example.com/foo.tgz") as d:
          # archive contents have been extracted to 'd'
          ...
      # d is automatically cleaned up.

    :param str url: URL of a .tgz or .tar.gz file to download.
    """
    with TemporaryDirectory(prefix="cot_helper") as d:
        logger.debug("Temporary directory is %s", d)
        logger.verbose("Downloading and extracting %s", url)
        response = requests.get(url, stream=True)
        tgz = os.path.join(d, 'helper.tgz')
        with open(tgz, 'wb') as f:
            shutil.copyfileobj(response.raw, f)
        del response
        logger.debug("Extracting %s", tgz)
        # the "with tarfile.open()..." construct isn't supported in 2.6
        tarf = tarfile.open(tgz, "r:gz")
        try:
            tarf.extractall(path=d)
        finally:
            tarf.close()
        try:
            yield d
        finally:
            logger.debug("Cleaning up temporary directory %s", d)


def get_checksum(path_or_obj, checksum_type):
    """Get the checksum of the given file.

    :param str path_or_obj: File path to checksum OR an opened file object
    :param str checksum_type: Supported values are 'md5' and 'sha1'.
    :return: String containing hexadecimal file checksum
    """
    # pylint: disable=redefined-variable-type
    if checksum_type == 'md5':
        h = hashlib.md5()
    elif checksum_type == 'sha1':
        h = hashlib.sha1()
    else:
        raise NotImplementedError(
            "No support for generating checksum type {0}"
            .format(checksum_type))

    # Is it a file or do we need to open it?
    try:
        path_or_obj.read(0)
        file_obj = path_or_obj
    except AttributeError:
        file_obj = open(path_or_obj, 'rb')

    try:
        while True:
            buf = file_obj.read(BLOCKSIZE)
            if len(buf) == 0:
                break
            h.update(buf)
    finally:
        if file_obj != path_or_obj:
            file_obj.close()

    return h.hexdigest()


def get_disk_format(file_path):
    """Get the disk image format of the given file.

    .. warning::
      If :attr:`file_path` refers to a file which is not a disk image at all,
      this function will return ``('raw', None)``.

    :param str file_path: Path to disk image file to inspect.
    :return: ``(format, subformat)``

      * ``format`` may be ``'vmdk'``, ``'raw'``, or ``'qcow2'``
      * ``subformat`` may be ``None``, or various strings for ``'vmdk'`` files.
    """
    file_format = QEMUIMG.get_disk_format(file_path)

    if file_format == 'vmdk':
        # Look at the VMDK file header to determine the sub-format
        with open(file_path, 'rb') as f:
            # The header contains a fun mix of binary and ASCII, so ignore
            # any errors in decoding binary data to strings
            header = f.read(1000).decode('ascii', 'ignore')
            # Detect the VMDK format from the output:
            match = re.search('createType="(.*)"', header)
            if not match:
                raise RuntimeError("Could not find VMDK 'createType' in the "
                                   "file header:\n{0}".format(header))
            vmdk_format = match.group(1)
        logger.info("VMDK sub-format is '%s'", vmdk_format)
        return (file_format, vmdk_format)
    else:
        # No known/applicable sub-format
        return (file_format, None)


def get_disk_capacity(file_path):
    """Get the storage capacity of the given disk image.

    :param str file_path: Path to disk image file to inspect
    :return: Disk capacity, in bytes
    """
    return QEMUIMG.get_disk_capacity(file_path)


def convert_disk_image(file_path, output_dir, new_format, new_subformat=None):
    """Convert the given disk image to the requested format/subformat.

    If the disk is already in this format then it is unchanged;
    otherwise, will convert to a new disk in the specified output_dir
    and return its path.

    Current supported conversions:

    * .vmdk (any format) to .vmdk (streamOptimized)
    * .img to .vmdk (streamOptimized)

    :param str file_path: Disk image file to inspect/convert
    :param str output_dir: Directory to place converted image into, if needed
    :param str new_format: Desired final format
    :param str new_subformat: Desired final subformat
    :return:
      * :attr:`file_path`, if no conversion was required
      * or a file path in :attr:`output_dir` containing the converted image

    :raise ValueUnsupportedError: if the :attr:`new_format` and/or
      :attr:`new_subformat` are not supported conversion targets.
    """
    curr_format, curr_subformat = get_disk_format(file_path)

    if curr_format == new_format and curr_subformat == new_subformat:
        logger.info("Disk image %s is already in '%s' format - "
                    "no conversion required.", file_path,
                    (new_format if not new_subformat else
                     (new_format + "," + new_subformat)))
        return file_path

    file_name = os.path.basename(file_path)
    (file_string, _) = os.path.splitext(file_name)

    new_file_path = None
    # any temporary file we should delete before returning
    temp_path = None

    if new_format == 'vmdk' and new_subformat == 'streamOptimized':
        new_file_path = os.path.join(output_dir, file_string + '.vmdk')
        # QEMU only supports streamOptimized images in versions >= 2.1.0
        if QEMUIMG.version >= StrictVersion("2.1.0"):
            new_file_path = QEMUIMG.convert_disk_image(
                file_path, output_dir, new_format, new_subformat)
        else:
            # Older versions of qemu-img don't support streamOptimized VMDKs,
            # so we have to use qemu-img + vmdktool to get the desired result.

            # We have to pass through raw format on the way, even if the
            # existing image is a non-streamOptimized vmdk.
            if curr_format != 'raw':
                # Use qemu-img to convert to raw format
                temp_path = QEMUIMG.convert_disk_image(
                    file_path, output_dir, 'raw')
                file_path = temp_path

            # Use vmdktool to convert raw image to stream-optimized VMDK
            new_file_path = VMDKTOOL.convert_disk_image(
                file_path, output_dir, new_format, new_subformat)

    else:
        raise NotImplementedError(
            "no support for converting disk to {0} / {1}"
            .format(new_format, new_subformat))

    logger.info("Successfully converted from (%s,%s) to (%s,%s)",
                curr_format, curr_subformat, new_format, new_subformat)

    if temp_path is not None:
        os.remove(temp_path)

    return new_file_path


def create_disk_image(file_path, file_format=None,
                      capacity=None, contents=None):
    """Create a new disk image at the requested location.

    Either :attr:`capacity` or :attr:`contents` or both must be specified.

    :param str file_path: Desired location of new disk image
    :param str file_format: Desired image format (if not specified, this will
      be derived from the file extension of :attr:`file_path`)

    :param capacity: Disk capacity. A string like '16M' or '1G'.
    :param list contents: List of file paths to package into the created image.
      If not specified, the image will be left blank and unformatted.
    """
    if not capacity and not contents:
        raise RuntimeError("Either capacity or contents must be specified!")

    if not file_format:
        file_format = guess_file_format_from_path(file_path)

    if not contents:
        QEMUIMG.create_blank_disk(file_path, capacity, file_format)
    elif file_format == 'iso':
        MKISOFS.create_iso(file_path, contents)
    elif file_format == 'raw' or file_format == 'img':
        FATDISK.create_raw_image(file_path, contents, capacity)
    else:
        # We could create a raw image then convert it to the
        # desired format but there's no use case for that at present.
        raise NotImplementedError(
            "unable to create disk of format {0} with the given contents"
            .format(file_format))


def install_file(src, dest):
    """Copy the given src to the given dest, using sudo if needed.

    :param str src: Source path.
    :param str dest: Destination path.
    :return: True
    """
    return Helper.install_file(src, dest)


def create_install_dir(directory, permissions=493):  # 493 == 0o755
    """Check whether the given target directory exists, and create if not.

    :param str directory: Directory to check/create.
    :param int permissions: Permissions bits to set on the directory.
    :return: True
    """
    return Helper.make_install_dir(directory, permissions)
