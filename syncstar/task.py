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


import signal
import subprocess
import traceback
from os import environ as envr
from time import sleep, time

from celery import Celery
from celery.exceptions import Ignore

from syncstar import __projname__, base, config
from syncstar.config import standard

taskmgmt = Celery(
    __projname__,
    broker=standard.broker_link,
    result_backend=standard.result_link
)


@taskmgmt.task(bind=True)
def wrap_diskdrop(self, diskindx: str, isosindx: str) -> dict:
    config.isos_config(envr["SYNCSTAR_ISOSYAML"])
    isosfile = standard.imdict[isosindx]["path"]
    diskfile = base.list_drives()[diskindx]["node"]

    # FOR DEBUGGING PURPOSES
    # Uncomment one of the following lines
    # diskfile = "/home/archdesk/tempdeletethisshit.img"
    # diskfile = "/dev/null"

    comd = ["dd", f"if={isosfile}", f"of={diskfile}", "status=progress"]
    proc = subprocess.Popen(comd, stderr=subprocess.PIPE)  # noqa : S603
    strt = time()
    done = 0

    while proc.poll() is None:
        sleep(1)
        proc.send_signal(signal.SIGUSR1)
        if diskindx in base.list_drives().keys():
            text = proc.stderr.readline().decode()
            if "records out" in text:
                done = text.split(" ")[0].split("+")[0]
                print(text)
                self.update_state(
                    state="WORKING",
                    meta={
                        "progress": done,
                        "time": {
                            "strt": strt,
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
                    "progress": done,
                    "time": {
                        "strt": strt,
                        "stop": time()
                    },
                    "finished": False
                }
            )
            proc.send_signal(signal.SIGTERM)
            raise Ignore()

    return {
        "progress": done,
        "time": {
            "strt": strt,
            "stop": time(),
        },
        "finished": True,
    }
