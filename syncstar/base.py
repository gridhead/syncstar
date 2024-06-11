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
    return datetime.now().astimezone().strftime("%X %x %Z")


def retrieve_disk_size(device: str) -> int:
    try:
        return int(
            subprocess.check_output(
                ["lsblk", "-b", "-n", "-o", "SIZE", f"{device}"]  # noqa : S603, S607
            ).decode().split("\n")[0])
    except subprocess.CalledProcessError:
        view.warning(f"Requested device '{device}' was not found")
        return 0


def list_drives() -> dict:
    """
    List storage devices according to the identification provided by the hexdigest of the SHA256
    hash of their hardware serial numbers of the respective storage devices
    """
    iterdict = {}
    for indx in pyudev.Context().list_devices(subsystem="block", DEVTYPE="disk"):
        if isinstance(indx.get("ID_BUS"), str):
            if "usb" in indx.get("ID_BUS"):
                iterdict[
                    sha256(indx.properties["ID_SERIAL_SHORT"].encode()).hexdigest()[0:8].upper()
                ] = {
                    "node": indx.device_node,
                    "name": {
                        "vendor": indx.properties["ID_VENDOR"],
                        "handle": indx.properties["ID_MODEL"],
                    },
                    "iden": indx.device_number,
                    "size": retrieve_disk_size(indx.device_node),
                }
    standard.dkdict = iterdict
    return iterdict
