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
from datetime import datetime
from hashlib import sha256
from logging.config import dictConfig
from time import sleep, time

from celery import Celery
from celery.exceptions import Ignore
from celery.signals import setup_logging

from syncstar import __projname__, base, util
from syncstar.config import standard
from syncstar.view import failure, general, success, warning
from syncstar.base import show_duration


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
    # diskfile = "/tmp/deletethis.img"
    # diskfile = "/dev/null"

    qant = util.CompletionConfirmation()
    # comd = ["dd", f"if={isosfile}", f"of={diskfile}", "status=progress"]
    comd = ["pv", "--direct-io", "--sync", "--format", "\"%{progress-amount-only} %{timer} %{eta} %{fineta} %{rate} %{average-rate} %{bytes}\"", f"{isosfile}", "--output", f"{diskfile}"]
    proc = subprocess.Popen(comd, stderr=subprocess.PIPE)  # noqa : S603
    iden = sha256(str(self.request.id).encode()).hexdigest()[0:8].upper()
    strt_time = time()
    curt_time = time()
    percentage = 0
    passed_time = "0 second(s)"
    approx_time = "0 second(s)"
    finish_time = "00:00:00 UTC"
    live_rate = "0.00B/s"
    mean_rate = "0.00B/s"
    syncedsize = "0B"

    warning(format_output(iden, curt_time-strt_time, "PENDING", f"Flashing '{isosfile}' to '{diskfile}'"))

    while proc.poll() is None:
        sleep(1)
        proc.send_signal(signal.SIGUSR1)
        curt_time = time()

        if diskindx in base.list_drives().keys():
            text = proc.stderr.readline().decode()
            print(text)

            """
            Example output
            23% 0:00:28 ETA 0:01:34 FIN 17:25:02 [ 835KiB/s] (19.0MiB/s)  546MiB
            """

            if "ETA" in text:
                unit = text.strip().split(" ")
                percentage = int(unit[0].replace("%", ""))
                passed_time = show_duration(*[int(item) for item in unit[1].split(":")])
                approx_time = show_duration(*[int(item) for item in unit[3].split(":")])
                finish_time = unit[5] + " " + datetime.now().astimezone().strftime("%Z")
                live_rate = text.split("]")[0].split("[")[1].strip()
                mean_rate = text.split(")")[0].split("(")[1].strip()
                syncedsize = unit[-1]
                qant.push(percentage)

                if bool(qant):
                    success(format_output(iden, curt_time-strt_time, "SUCCESS", f"Long running task safely terminated after {standard.poll} checks"))  # noqa : E501
                    self.update_state(
                        state="SUCCESS",
                        meta={
                            "progress": {
                                "percentage": percentage,
                                "syncedsize": syncedsize,
                            },
                            "rate": {
                                "live_rate": live_rate,
                                "mean_rate": mean_rate
                            },
                            "time": {
                                "duration": {
                                    "strt_time": strt_time,
                                    "curt_time": curt_time
                                },
                                "complete": {
                                    "passed_time": passed_time,
                                    "approx_time": approx_time,
                                    "finish_time": finish_time,
                                },
                            },
                            "finished": True,
                        }
                    )
                    proc.send_signal(signal.SIGTERM)
                    raise Ignore()

                general(format_output(iden, curt_time-strt_time, "WORKING", text.replace("\n", "")))
                self.update_state(
                    state="WORKING",
                    meta={
                        "progress": {
                            "percentage": percentage,
                            "syncedsize": syncedsize,
                        },
                        "rate": {
                            "live_rate": live_rate,
                            "mean_rate": mean_rate
                        },
                        "time": {
                            "duration": {
                                "strt_time": strt_time,
                                "curt_time": curt_time
                            },
                            "complete": {
                                "passed_time": passed_time,
                                "approx_time": approx_time,
                                "finish_time": finish_time,
                            },
                        },
                        "finished": False,
                    }
                )

        else:
            failure(format_output(iden, curt_time-strt_time, "FAILURE", "Unsafe removal of storage device can cause hardware damage"))  # noqa : E501
            self.update_state(
                state="FAILURE",
                meta={
                    "exc_type": "Key",
                    "exc_message": traceback.format_exc().split("\n"),
                    "progress": {
                        "percentage": percentage,
                        "syncedsize": syncedsize,
                    },
                    "rate": {
                        "live_rate": live_rate,
                        "mean_rate": mean_rate
                    },
                    "time": {
                        "duration": {
                            "strt_time": strt_time,
                            "curt_time": curt_time
                        },
                        "complete": {
                            "passed_time": passed_time,
                            "approx_time": approx_time,
                            "finish_time": finish_time,
                        },
                    },
                    "finished": False,
                }
            )
            proc.send_signal(signal.SIGTERM)
            raise Ignore()

    success(format_output(iden, curt_time-strt_time, "SUCCESS", "Please remove the storage device and attempt booting from it"))  # noqa : E501
    return {
        "progress": {
            "percentage": percentage,
            "syncedsize": syncedsize,
        },
        "rate": {
            "live_rate": live_rate,
            "mean_rate": mean_rate
        },
        "time": {
            "duration": {
                "strt_time": strt_time,
                "curt_time": curt_time
            },
            "complete": {
                "passed_time": passed_time,
                "approx_time": approx_time,
                "finish_time": finish_time,
            },
        },
        "finished": True,
    }
