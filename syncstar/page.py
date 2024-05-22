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


import os.path

from os import urandom

from flask import Flask, render_template, abort

from syncstar.config import standard, manifest
from syncstar import __versdata__
from syncstar.auth import checkpoint
from syncstar.base import list_drives, show_time
from syncstar.make import sync_drives
from syncstar import view

from time import time


main = Flask(
    import_name="SyncStar",
    template_folder=os.path.abspath("syncstar/frontend/template"),
    static_folder=os.path.abspath("syncstar/frontend/static")
)


@main.route("/", methods=["GET"])
def home() -> str:
    return render_template(
        "home.html",
        versdata=__versdata__,
        rqstcode=standard.code,
        timesecs=standard.period,
        icondict=manifest.icondict,
    )


@main.route("/kick/<rqstcode>/<diskindx>/<isosindx>", methods=["GET"])
@checkpoint
def kick(rqstcode: str, diskindx: str, isosindx: str) -> dict:
    iterdict = list_drives()
    if diskindx in iterdict:
        if isosindx in standard.imdict:
            if diskindx not in standard.lockls:
                if standard.imdict[isosindx]["size"] < iterdict[diskindx]["size"]:
                    iden = urandom(4).hex().upper()
                    standard.joblst[iden] = {
                        "disk": diskindx,
                        "isos": isosindx,
                        "mood": "WAITING",
                        "time": {
                            "strt": time(),
                            "stop": 0,
                        },
                    }
                    print("JOB START", standard.joblst[iden]["time"]["strt"])
                    standard.lockls.append(diskindx)
                    return sync_drives(diskindx, isosindx)
                else:
                    abort(422, f"Insufficient capacity")
            else:
                abort(400, f"Disk locked: {diskindx}")
        else:
            abort(404, f"No such image: {isosindx}")
    else:
        abort(404, f"No such disk: {diskindx}")


@main.route("/scan/<rqstcode>/<diskindx>", methods=["GET"])
@checkpoint
def scan(rqstcode: str, diskindx: str) -> dict:
    iterdict = list_drives()
    if diskindx in iterdict:
        if diskindx not in standard.lockls:
            imdict = standard.imdict
            for indx in imdict:
                if imdict[indx]["size"] < iterdict[diskindx]["size"]:
                    imdict[indx]["bool"] = True
                else:
                    imdict[indx]["bool"] = False
            return {
                "indx": diskindx,
                "disk": standard.dkdict[diskindx],
                "isos": imdict,
            }
        else:
            abort(400, f"Disk locked: {diskindx}")
    else:
        abort(404, f"No such disk: {diskindx}")


@main.route("/read/<rqstcode>", methods=["GET"])
@checkpoint
def read(rqstcode: str) -> dict:
    joblst = {}
    diskdict = list_drives()

    # Populate a dictionary of all the storage devices regardless of they are connected currently or were connected in the past
    for jndx in diskdict:
        standard.hsdict[jndx] = diskdict[jndx]

    disk_detect = True

    for indx in standard.joblst.keys():
        # TODO - Add more conditions

        jobsindx = standard.joblst[indx]

        if (
            # Images archive is being currently synchronized to the storage device
            # STATE is not FAILURE, STORAGE DEVICE is CONNECTED and STORAGE DEVICE is LOCKED
            jobsindx["mood"] != "FAILURE" and jobsindx["disk"] in diskdict and jobsindx["disk"] in standard.lockls
        ) or (
            # Storage device being plugged in after the images archive failed to synchronize ONE TIMES to the storage device due to the storage device being removed during the process
            # STATE is FAILURE, STORAGE DEVICE is not CONNECTED and STORAGE DEVICE is not LOCKED
            jobsindx["mood"] == "FAILURE" and jobsindx["disk"] not in diskdict and jobsindx["disk"] not in standard.lockls
        ) or (
            # Storage device being plugged in after the images archive failed to synchronize TWO TIMES to the storage device due to the storage device being removed during the process
            # STATE is FAILURE and STORAGE DEVICE is CONNECTED
            jobsindx["mood"] == "FAILURE" and jobsindx["disk"] in diskdict
        ):
            joblst[indx] = {
                "disk": f"{standard.hsdict[jobsindx['disk']]['name']['vendor']} {standard.hsdict[jobsindx['disk']]['name']['handle']}",
                "isos": standard.imdict[jobsindx["isos"]]["name"],
                "time": (standard.joblst[indx]["time"]["stop"] - standard.joblst[indx]["time"]["strt"]) if standard.joblst[indx]["mood"] == "FAILURE" else (time() - standard.joblst[indx]["time"]["strt"]),
                "mood": jobsindx["mood"],
            }

            # Set flags for whenever the operational storage devices are detected properly
            disk_detect = True

        else:
            if jobsindx["mood"] != "FAILURE":
                # Placeholder condition above - Gotta get the parent conditions right and then I can remove this placeholder condition
                jobsindx["mood"] = "FAILURE"
                jobsindx["time"]["stop"] = time()
                if jobsindx["disk"] in standard.lockls:
                    standard.lockls.remove(jobsindx["disk"])

            # Set flags for whenever the operational storage devices are not detected properly
            disk_detect = False

    if disk_detect:
        return {
            "time": show_time(),
            "devs": diskdict,
            "jobs": joblst,
        }
    else:
        view.failure("Storage device was removed during synchronization")
        abort(500, f"Storage device removed")


def work() -> None:
    main.run(
        host="0.0.0.0",
        port=standard.port,
        debug=standard.repair
    )


"""
WAITING
RUNNING
SUCCESS
FAILURE
"""
