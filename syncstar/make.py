"""
SyncStar
Copyright (C) 2024 Akashdeep Dhar

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
details.

You should have received a copy of the GNU General Public License along with
this program.  If not, see <https://www.gnu.org/licenses/>.

Any Red Hat trademarks that are incorporated in the source code or
documentation are not subject to the GNU General Public License and may only
be used or replicated with the express permission of Red Hat, Inc.
"""


from syncstar.config import view

from syncstar.config import standard

from syncstar.base import list_drives

from os import path, sendfile

from time import time, sleep


def sync_drives(diskindx: str, isosindx: str) -> dict:
    try:
        """
        with open(standard.imdict[isosindx]["path"], "rb") as isosfile:
            with open(list_drives()[diskindx]["node"], "wb") as diskfile:
                size = path.getsize(standard.imdict[isosindx]["path"])
                offs = 0
                view.warning(f"Synchronizing '{isosfile}' to '{diskindx}'...")
                while offs < size:
                    sent = sendfile(diskfile.fileno(), isosfile.fileno(), offs, size - offs)
                    if sent == 0:
                        break
                    offs += sent
                    view.general(f"Synchronizing {sent} bytes out of {size} bytes...")
                standard.lockls[diskindx]["time"]["stop"] = time()
        """
        # sleep(5)
        # standard.lockls.remove(diskindx)
        return {
            "status": "complete",
            "reason": "complete",
        }
    except Exception as expt:
        view.failure(f"Failed to synchronize '{isosindx}' to '{diskindx}'")
        view.failure(f"Exception : {expt}")
        return {
            "status": "collapse",
            "reason": f"{expt}"
        }
