"""
SyncStar
Copyright (C) 2024 Akashdeep Dhar

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU Affero General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more
details.

You should have received a copy of the GNU Affero General Public License along
with this program.  If not, see <https://www.gnu.org/licenses/>.

Any Red Hat trademarks that are incorporated in the codebase or documentation
are not subject to the GNU Affero General Public License and may only be used
or replicated with the express permission of Red Hat, Inc.
"""


import subprocess
from datetime import datetime
from hashlib import sha256

import pyudev

from syncstar import view
from syncstar.config import standard


def show_time() -> str:
    """
    Returns the current local date and time in a human-readable string format

    The format includes `time` in `HH:MM:SS` format, `date` in `MM/DD/YY` format and timezone
    abbreviation. The time is displayed according to the system's default local timezone.

    :return: Formatted current local date and time
    """
    return datetime.now().astimezone().strftime("%X %x %Z")


def retrieve_disk_size(device: str) -> int:
    """
    Retrieves the size of a disk device in bytes

    Uses the `lsblk` command to obtain the size of the specified device in bytes. If the device
    is not found or an error occurs, a warning is displayed, and the function returns 0.

    :param device: Path to the device (e.g. "/dev/sda")
    :return: Size of the device in bytes, or 0 if the device is not found
    """
    try:
        return int(
            subprocess.check_output(  # noqa: S603
                ["lsblk", "-b", "-n", "-o", "SIZE", f"{device}"]  # noqa : S603, S607
            ).decode().split("\n")[0])
    except subprocess.CalledProcessError:
        view.warning(f"Requested device '{device}' was not found")
        return 0


def list_drives() -> dict:
    """
    Lists storage devices connected to the system.

    This function identifies storage devices using the first 8 characters of the SHA256 hash
    of their hardware serial numbers. Only devices connected via USB are included. The resulting
    dictionary is also stored in `standard.dkdict`. Each device's details are stored in a
    dictionary with the following keys:

    - `node`: Device node (e.g., `/dev/sda`)
    - `name`: A dictionary containing the vendor and model name of the device
    - `iden`: Device identifier
    - `size`: Size of the device in bytes, obtained using `retrieve_disk_size`

    :return: Dictionary mapping device hashes to their details
    """
    iterdict = {}
    for indx in pyudev.Context().list_devices(subsystem="block", DEVTYPE="disk"):
        if isinstance(indx.get("ID_BUS"), str):
            if "usb" in indx.get("ID_BUS"):
                iterdict[
                    sha256(
                        indx.properties.get("ID_SERIAL_SHORT", "Void").encode()
                    ).hexdigest()[0:8].upper()
                ] = {
                    "node": indx.device_node,
                    "name": {
                        "vendor": indx.properties.get("ID_VENDOR", "Void"),
                        "handle": indx.properties.get("ID_MODEL", "Void"),
                    },
                    "iden": indx.device_number,
                    "size": retrieve_disk_size(indx.device_node),
                }
    standard.dkdict = iterdict
    return iterdict
