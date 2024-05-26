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

from celery.exceptions import Ignore

import traceback

from syncstar.config import view

from syncstar.config import standard

from syncstar.base import list_drives

from os import path, sendfile

import random

from time import time, sleep

from celery import Celery, states

from syncstar.config import isos_config


taskmgmt = Celery("SyncStar", broker=standard.broker_link, result_backend=standard.result_link)


@taskmgmt.task(bind=True)
def sync_drives(self, diskindx: str, isosindx: str) -> dict:
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
    isos_config("/home/archdesk/Projects/syncstar/syncstar/config/images.yml")
    strttime = time()
    for indx in range(100):
        if diskindx in list_drives().keys():
            self.update_state(
                state="WORKING",
                meta={
                    "progress": indx,
                    "complete": 100,
                    "time": {
                        "strt": strttime,
                        "stop": time()
                    },
                    "finished": False,
                }
            )
        else:
            print("DEVICE REMOVED")
            self.update_state(
                state="FAILURE",
                meta={
                    "exc_type": "Key",
                    "exc_message": traceback.format_exc().split("\n"),
                    "result": "Stuff",
                    "progress": 0,
                    "complete": 100,
                    "time": {
                        "strt": strttime,
                        "stop": time()
                    },
                    "finished": False,
                }
            )
            raise Ignore()
        sleep(0.25)
    return {
        "progress": 100,
        "complete": 100,
        "time": {
            "strt": strttime,
            "stop": time()
        },
        "finished": True,
    }
