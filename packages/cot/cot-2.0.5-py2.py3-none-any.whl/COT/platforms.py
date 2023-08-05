#!/usr/bin/env python
#
# platforms.py - Module for methods related to variations between
#                guest platforms (Cisco CSR1000V, Cisco IOS XRv, etc.)
#
# October 2013, Glenn F. Matthews
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

"""Handles behavior that varies between guest platforms.

**Functions**

.. autosummary::
  :nosignatures:

  platform_from_product_class

**Classes**

.. autosummary::
  :nosignatures:

  GenericPlatform
  CSR1000V
  IOSv
  IOSXRv
  IOSXRvRP
  IOSXRvLC
  IOSXRv9000
  NXOSv

**Constants**

.. autosummary::
  PRODUCT_PLATFORM_MAP
"""

import logging

from .data_validation import ValueUnsupportedError
from .data_validation import ValueTooLowError, ValueTooHighError
from .data_validation import NIC_TYPES

logger = logging.getLogger(__name__)


def is_known_product_class(product_class):
    """Determine if the given product class string is a known one."""
    return product_class in PRODUCT_PLATFORM_MAP


def platform_from_product_class(product_class):
    """Get the class of Platform corresponding to a product class string."""
    if product_class is None:
        return GenericPlatform
    if is_known_product_class(product_class):
        return PRODUCT_PLATFORM_MAP[product_class]
    logger.warning("Unrecognized product class '%s' - known classes "
                   "are %s. Treating as a generic platform",
                   product_class, PRODUCT_PLATFORM_MAP.keys())
    return GenericPlatform


def valid_range(label, value, min_val, max_val):
    """Raise an exception if the value is not in the valid range."""
    if min_val is not None and value < min_val:
        raise ValueTooLowError(label, value, min_val)
    elif max_val is not None and value > max_val:
        raise ValueTooHighError(label, value, max_val)
    return True


class GenericPlatform(object):
    """Generic class for operations that depend on guest platform.

    To be used whenever the guest is unrecognized or does not need
    special handling.
    """

    PLATFORM_NAME = "(unrecognized platform, generic)"

    # Default file name for text configuration file to embed
    CONFIG_TEXT_FILE = 'config.txt'
    # Most platforms do not support a secondary configuration file
    SECONDARY_CONFIG_TEXT_FILE = None
    # Most platforms do not support configuration properties in the environment
    LITERAL_CLI_STRING = 'config'

    # Most platforms use a CD-ROM for bootstrap configuration
    BOOTSTRAP_DISK_TYPE = 'cdrom'

    SUPPORTED_NIC_TYPES = NIC_TYPES

    @classmethod
    def controller_type_for_device(cls, _device_type):
        """Get the default controller type for the given device type."""
        # For most platforms IDE is the correct default.
        return 'ide'

    @classmethod
    def guess_nic_name(cls, nic_number):
        """Guess the name of the Nth NIC for this platform.

        .. note:: This method counts from 1, not from 0!
        """
        return "Ethernet" + str(nic_number)

    @classmethod
    def validate_cpu_count(cls, cpus):
        """Throw an error if the number of CPUs is not a supported value."""
        valid_range("CPUs", cpus, 1, None)

    @classmethod
    def validate_memory_amount(cls, mebibytes):
        """Throw an error if the amount of RAM is not supported."""
        valid_range("RAM", mebibytes, 1, None)

    @classmethod
    def validate_nic_count(cls, count):
        """Throw an error if the number of NICs is not supported."""
        valid_range("NIC count", count, 0, None)

    @classmethod
    def validate_nic_type(cls, type_string):
        """Throw an error if the NIC type string is not supported.

        .. seealso::
           - :func:`COT.data_validation.canonicalize_nic_subtype`
           - :data:`COT.data_validation.NIC_TYPES`
        """
        if type_string not in cls.SUPPORTED_NIC_TYPES:
            raise ValueUnsupportedError("NIC type", type_string,
                                        cls.SUPPORTED_NIC_TYPES)

    @classmethod
    def validate_nic_types(cls, type_list):
        """Throw an error if any NIC type string in the list is unsupported."""
        for type_string in type_list:
            cls.validate_nic_type(type_string)

    @classmethod
    def validate_serial_count(cls, count):
        """Throw an error if the number of serial ports is not supported."""
        valid_range("serial port count", count, 0, None)


class IOSXRv(GenericPlatform):
    """Platform-specific logic for Cisco IOS XRv platform."""

    PLATFORM_NAME = "Cisco IOS XRv"

    CONFIG_TEXT_FILE = 'iosxr_config.txt'
    SECONDARY_CONFIG_TEXT_FILE = 'iosxr_config_admin.txt'
    LITERAL_CLI_STRING = None
    SUPPORTED_NIC_TYPES = ["E1000", "virtio"]

    @classmethod
    def guess_nic_name(cls, nic_number):
        """MgmtEth0/0/CPU0/0, GigabitEthernet0/0/0/0, Gig0/0/0/1, etc."""
        if nic_number == 1:
            return "MgmtEth0/0/CPU0/0"
        else:
            return "GigabitEthernet0/0/0/" + str(nic_number - 2)

    @classmethod
    def validate_cpu_count(cls, cpus):
        """IOS XRv supports 1-8 CPUs."""
        valid_range("CPUs", cpus, 1, 8)

    @classmethod
    def validate_memory_amount(cls, mebibytes):
        """Minimum 3 GiB, max 8 GiB of RAM."""
        if mebibytes < 3072:
            raise ValueTooLowError("RAM", str(mebibytes) + " MiB", "3 GiB")
        elif mebibytes > 8192:
            raise ValueTooHighError("RAM", str(mebibytes) + " MiB", " 8GiB")

    @classmethod
    def validate_nic_count(cls, count):
        """IOS XRv requires at least one NIC."""
        valid_range("NIC count", count, 1, None)

    @classmethod
    def validate_serial_count(cls, count):
        """IOS XRv supports 1-4 serial ports."""
        valid_range("serial ports", count, 1, 4)


class IOSXRvRP(IOSXRv):
    """Platform-specific logic for Cisco IOS XRv HA-capable RP."""

    PLATFORM_NAME = "Cisco IOS XRv route processor card"

    @classmethod
    def guess_nic_name(cls, nic_number):
        """Fabric and management only.

        * fabric
        * MgmtEth0/{SLOT}/CPU0/0
        """
        if nic_number == 1:
            return "fabric"
        else:
            return "MgmtEth0/{SLOT}/CPU0/" + str(nic_number - 2)

    @classmethod
    def validate_nic_count(cls, count):
        """Fabric plus an optional management NIC."""
        valid_range("NIC count", count, 1, 2)


class IOSXRvLC(IOSXRv):
    """Platform-specific logic for Cisco IOS XRv line card."""

    PLATFORM_NAME = "Cisco IOS XRv line card"

    # No bootstrap config for LCs - they inherit from the RP
    CONFIG_TEXT_FILE = None
    SECONDARY_CONFIG_TEXT_FILE = None

    @classmethod
    def guess_nic_name(cls, nic_number):
        """Fabric interface plus slot-appropriate GigabitEthernet interfaces.

        * fabric
        * GigabitEthernet0/{SLOT}/0/0
        * GigabitEthernet0/{SLOT}/0/1
        * etc.
        """
        if nic_number == 1:
            return "fabric"
        else:
            return "GigabitEthernet0/{SLOT}/0/" + str(nic_number - 2)

    @classmethod
    def validate_serial_count(cls, count):
        """No serial ports are needed but up to 4 can be used for debugging."""
        valid_range("serial ports", count, 0, 4)


class IOSXRv9000(IOSXRv):
    """Platform-specific logic for Cisco IOS XRv 9000 platform."""

    PLATFORM_NAME = "Cisco IOS XRv 9000"
    SUPPORTED_NIC_TYPES = ["E1000", "virtio", "VMXNET3"]

    @classmethod
    def guess_nic_name(cls, nic_number):
        """MgmtEth0/0/CPU0/0, CtrlEth, DevEth, GigabitEthernet0/0/0/0, etc."""
        if nic_number == 1:
            return "MgmtEth0/0/CPU0/0"
        elif nic_number == 2:
            return "CtrlEth"
        elif nic_number == 3:
            return "DevEth"
        else:
            return "GigabitEthernet0/0/0/" + str(nic_number - 4)

    @classmethod
    def validate_cpu_count(cls, cpus):
        """Minimum 1, maximum 32 CPUs."""
        valid_range("CPUs", cpus, 1, 32)

    @classmethod
    def validate_memory_amount(cls, mebibytes):
        """Minimum 8 GiB, maximum 32 GiB."""
        if mebibytes < 8192:
            raise ValueTooLowError("RAM", str(mebibytes) + " MiB", "8 GiB")
        elif mebibytes > 32768:
            raise ValueTooHighError("RAM", str(mebibytes) + " MiB", "32 GiB")

    @classmethod
    def validate_nic_count(cls, count):
        """IOS XRv 9000 requires at least 4 NICs."""
        valid_range("NIC count", count, 4, None)


class CSR1000V(GenericPlatform):
    """Platform-specific logic for Cisco CSR1000V platform."""

    PLATFORM_NAME = "Cisco CSR1000V"

    CONFIG_TEXT_FILE = 'iosxe_config.txt'
    LITERAL_CLI_STRING = 'ios-config'
    # CSR1000v doesn't 'officially' support E1000, but it mostly works
    SUPPORTED_NIC_TYPES = ["E1000", "virtio", "VMXNET3"]

    @classmethod
    def controller_type_for_device(cls, device_type):
        """CSR1000V uses SCSI for hard disks and IDE for CD-ROMs."""
        if device_type == 'harddisk':
            return 'scsi'
        elif device_type == 'cdrom':
            return 'ide'
        else:
            return super(CSR1000V, cls).controller_type_for_device(device_type)

    @classmethod
    def guess_nic_name(cls, nic_number):
        """GigabitEthernet1, GigabitEthernet2, etc.

        .. warning::
          In all current CSR releases, NIC names start at "GigabitEthernet1".
          Some early versions started at "GigabitEthernet0" but we don't
          support that.
        """
        return "GigabitEthernet" + str(nic_number)

    @classmethod
    def validate_cpu_count(cls, cpus):
        """CSR1000V supports 1, 2, or 4 CPUs."""
        valid_range("CPUs", cpus, 1, 4)
        if cpus != 1 and cpus != 2 and cpus != 4:
            raise ValueUnsupportedError("CPUs", cpus, [1, 2, 4])

    @classmethod
    def validate_memory_amount(cls, mebibytes):
        """Minimum 2.5 GiB, max 8 GiB."""
        if mebibytes < 2560:
            raise ValueTooLowError("RAM", str(mebibytes) + " MiB", "2.5 GiB")
        elif mebibytes > 8192:
            raise ValueTooHighError("RAM", str(mebibytes) + " MiB", "8 GiB")

    @classmethod
    def validate_nic_count(cls, count):
        """CSR1000V requires 3 NICs and supports up to 26."""
        valid_range("NICs", count, 3, 26)

    @classmethod
    def validate_serial_count(cls, count):
        """CSR1000V supports 0-2 serial ports."""
        valid_range("serial ports", count, 0, 2)


class IOSv(GenericPlatform):
    """Platform-specific logic for Cisco IOSv."""

    PLATFORM_NAME = "Cisco IOSv"

    CONFIG_TEXT_FILE = 'ios_config.txt'
    LITERAL_CLI_STRING = None
    # IOSv has no CD-ROM driver so bootstrap configs must be provided on disk.
    BOOTSTRAP_DISK_TYPE = 'harddisk'
    SUPPORTED_NIC_TYPES = ["E1000"]

    @classmethod
    def guess_nic_name(cls, nic_number):
        """GigabitEthernet0/0, GigabitEthernet0/1, etc."""
        return "GigabitEthernet0/" + str(nic_number - 1)

    @classmethod
    def validate_cpu_count(cls, cpus):
        """IOSv only supports a single CPU."""
        valid_range("CPUs", cpus, 1, 1)

    @classmethod
    def validate_memory_amount(cls, mebibytes):
        """IOSv has minimum 192 MiB (with minimal feature set), max 3 GiB."""
        if mebibytes < 192:
            raise ValueTooLowError("RAM", str(mebibytes) + " MiB", "192 MiB")
        elif mebibytes < 384:
            # Warn but allow
            logger.warning("Less than 384MiB of RAM may not be sufficient "
                           "for some IOSv feature sets")
        elif mebibytes > 3072:
            raise ValueTooHighError("RAM", str(mebibytes) + " MiB", "3 GiB")

    @classmethod
    def validate_nic_count(cls, count):
        """IOSv supports up to 16 NICs."""
        valid_range("NICs", count, 0, 16)

    @classmethod
    def validate_serial_count(cls, count):
        """IOSv requires 1-2 serial ports."""
        valid_range("serial ports", count, 1, 2)


class NXOSv(GenericPlatform):
    """Platform-specific logic for Cisco NX-OSv (Titanium)."""

    PLATFORM_NAME = "Cisco NX-OSv"

    CONFIG_TEXT_FILE = 'nxos_config.txt'
    LITERAL_CLI_STRING = None
    SUPPORTED_NIC_TYPES = ["E1000", "virtio"]

    @classmethod
    def guess_nic_name(cls, nic_number):
        """NX-OSv names its NICs a bit interestingly...

        * mgmt0
        * Ethernet2/1
        * Ethernet2/2
        * ...
        * Ethernet2/48
        * Ethernet3/1
        * Ethernet3/2
        * ...
        """
        if nic_number == 1:
            return "mgmt0"
        else:
            return ("Ethernet{0}/{1}".format((nic_number - 2) // 48 + 2,
                                             (nic_number - 2) % 48 + 1))

    @classmethod
    def validate_cpu_count(cls, cpus):
        """NX-OSv requires 1-8 CPUs."""
        valid_range("CPUs", cpus, 1, 8)

    @classmethod
    def validate_memory_amount(cls, mebibytes):
        """NX-OSv requires 2-8 GiB of RAM."""
        if mebibytes < 2048:
            raise ValueTooLowError("RAM", str(mebibytes) + " MiB", "2 GiB")
        elif mebibytes > 8192:
            raise ValueTooHighError("RAM", str(mebibytes) + " MiB", "8 GiB")

    @classmethod
    def validate_serial_count(cls, count):
        """NX-OSv requires 1-2 serial ports."""
        valid_range("serial ports", count, 1, 2)

PRODUCT_PLATFORM_MAP = {
    'com.cisco.csr1000v':    CSR1000V,
    'com.cisco.iosv':        IOSv,
    'com.cisco.nx-osv':      NXOSv,
    'com.cisco.ios-xrv':     IOSXRv,
    'com.cisco.ios-xrv.rp':  IOSXRvRP,
    'com.cisco.ios-xrv.lc':  IOSXRvLC,
    'com.cisco.ios-xrv9000': IOSXRv9000,
    # Some early releases of IOS XRv 9000 used the
    # incorrect string 'com.cisco.ios-xrv64'.
    'com.cisco.ios-xrv64':   IOSXRv9000,
}
"""Mapping of known product class strings to Platform classes."""
