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
from hashlib import sha256
from logging.config import dictConfig
from time import sleep, time

from celery import Celery
from celery.exceptions import Ignore
from celery.signals import setup_logging

from syncstar import __projname__, base, util
from syncstar.config import standard
from syncstar.view import failure, general, success, warning

taskmgmt = Celery(
    __projname__,
    broker=standard.broker_link,
    result_backend=standard.result_link
)


@setup_logging.connect
def config_logger(*args, **kwargs):
    dictConfig(standard.logrconf)


def format_output(
        iden: str = "00000000",
        secs: float = 0.00,
        head: str = "ZERO",
        data: str = "ZERO"
) -> str:
    return f"[{iden}] [{head}] {secs:.2f}s - {data}"


@taskmgmt.task(bind=True)
def wrap_diskdrop(self, diskindx: str, isosindx: str) -> dict:
    isosfile = standard.imdict[isosindx]["path"]
    diskfile = base.list_drives()[diskindx]["node"]

    # FOR DEBUGGING PURPOSES
    # Uncomment one of the following lines
    # diskfile = "/home/archdesk/tempdeletethisshit.img"
    # diskfile = "/dev/null"

    qant = util.CompletionConfirmation()
    comd = ["dd", f"if={isosfile}", f"of={diskfile}", "status=progress"]
    proc = subprocess.Popen(comd, stderr=subprocess.PIPE, text=True)  # noqa : S603
    iden = sha256(str(self.request.id).encode()).hexdigest()[0:8].upper()
    strt, curt = time(), time()
    done, rate = 0, "0.00 B/s"

    warning(format_output(iden, curt-strt, "PENDING", f"Flashing '{isosfile}' to '{diskfile}'"))

    while proc.poll() is None:
        sleep(1)
        proc.send_signal(signal.SIGUSR1)
        curt = time()

        if diskindx in base.list_drives().keys():
            text = proc.stderr.readline()

            if "records out" in text:
                done = int(text.split(" ")[0].split("+")[0])
                qant.push(done)

            if "bytes" and "copied" in text:
                rate = text.split(",")[-1].strip()

            if bool(qant):
                success(format_output(iden, curt-strt, "SUCCESS", f"Long running task safely terminated after {standard.poll} checks"))  # noqa : E501
                self.update_state(
                    state="SUCCESS",
                    meta={
                        "rate": rate,
                        "time": {
                            "strt": strt,
                            "stop": curt
                        },
                        "finished": True,
                    }
                )
                proc.send_signal(signal.SIGTERM)
                raise Ignore()

            sanctified = text.replace("\n", "")
            general(format_output(iden, curt-strt, "WORKING", f"{rate} {sanctified}"))
            self.update_state(
                state="WORKING",
                meta={
                    "rate": rate,
                    "time": {
                        "strt": strt,
                        "stop": curt
                    },
                    "finished": False,
                }
            )

        else:
            failure(format_output(iden, curt-strt, "FAILURE", "Unsafe removal of storage device can cause hardware damage"))  # noqa : E501
            self.update_state(
                state="FAILURE",
                meta={
                    "exc_type": "Key",
                    "exc_message": traceback.format_exc().split("\n"),
                    "rate": rate,
                    "time": {
                        "strt": strt,
                        "stop": curt
                    },
                    "finished": False,
                }
            )
            proc.send_signal(signal.SIGTERM)
            raise Ignore()

    success(format_output(iden, curt-strt, "SUCCESS", "Please remove the storage device and attempt booting from it"))  # noqa : E501
    return {
        "rate": rate,
        "time": {
            "strt": strt,
            "stop": curt
        },
        "finished": True,
    }
