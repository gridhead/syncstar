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


from os import urandom
from time import time

from flask import abort, render_template

from syncstar import __versdata__, base, task
from syncstar.auth import checkpoint
from syncstar.config import manifest, standard
from syncstar.dyno import main


@main.route("/", methods=["GET"])
def home() -> str:
    return render_template(
        "home.html",
        versdata=__versdata__,
        rqstcode=standard.code,
        timesecs=standard.period,
        icondict=manifest.icondict,
        isosdict=standard.imdict,
    )


@main.route("/kick/<rqstcode>/<diskindx>/<isosindx>", methods=["GET"])
@checkpoint
def kick(rqstcode: str, diskindx: str, isosindx: str) -> dict:
    iterdict = base.list_drives()
    if diskindx in iterdict:
        if isosindx in standard.imdict:
            if diskindx not in standard.lockls:
                if standard.imdict[isosindx]["size"] < iterdict[diskindx]["size"]:
                    iden = urandom(4).hex().upper()
                    unit = task.wrap_diskdrop.apply_async(args=[diskindx, isosindx])
                    standard.joblst[iden] = {
                        "disk": diskindx,
                        "isos": isosindx,
                        "time": {
                            "strt": time(),
                            "stop": time(),
                        },
                        "task": unit.id,
                        "rcrd": 0,
                    }
                    standard.lockls.append(diskindx)
                    return {
                        "location": unit.id,
                    }
                else:
                    abort(422, "Insufficient capacity")
            else:
                abort(400, f"Disk locked: {diskindx}")
        else:
            abort(404, f"No such image: {isosindx}")
    else:
        abort(404, f"No such disk: {diskindx}")


@main.route("/scan/<rqstcode>/<diskindx>", methods=["GET"])
@checkpoint
def scan(rqstcode: str, diskindx: str) -> dict:
    iterdict = base.list_drives()
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
    diskdict = base.list_drives()

    # Populate a dictionary of all the storage devices regardless of
    # they are connected currently or were connected in the past
    for jndx in diskdict:
        standard.hsdict[jndx] = diskdict[jndx]

    tounlock = {}

    for indx in standard.joblst.keys():
        data = standard.joblst[indx]
        unit = task.wrap_diskdrop.AsyncResult(str(data["task"]).encode())
        joblst[indx] = {
            "disk": f"{standard.hsdict[data['disk']]['name']['vendor']} {standard.hsdict[data['disk']]['name']['handle']}",  # noqa : E501
            "isos": standard.imdict[data["isos"]]["name"],
            "mood": unit.state
        }
        if unit.state == "PENDING":
            # Conditions - PENDING
            joblst[indx]["time"] = time() - data["time"]["strt"]
            joblst[indx]["done"] = False
            joblst[indx]["rcrd"] = 0
            if data["disk"] in standard.lockls:
                tounlock[data["disk"]] = False
        elif unit.state == "FAILURE":
            # Conditions - FAILURE
            joblst[indx]["time"] = data["time"]["stop"] - data["time"]["strt"]
            joblst[indx]["done"] = False
            joblst[indx]["rcrd"] = data["rcrd"]
            if data["disk"] in standard.lockls:
                tounlock[data["disk"]] = True
        else:
            # Conditions - SUCCESS and WORKING
            joblst[indx]["time"] = unit.info.get("time").get("stop", 0) - data["time"]["strt"]
            joblst[indx]["done"] = unit.info.get("finished", True)
            joblst[indx]["rcrd"] = unit.info.get("progress", 0)
            standard.joblst[indx]["rcrd"] = unit.info.get("progress", 0)
            standard.joblst[indx]["time"]["stop"] = unit.info.get("time").get("stop", 0)
            if data["disk"] in standard.lockls:
                if unit.state == "WORKING":
                    tounlock[data["disk"]] = False
                elif unit.state == "SUCCESS":
                    tounlock[data["disk"]] = True

    # Set flags for whenever the operational storage devices are removed during synchronization
    for indx in tounlock.keys():
        if tounlock[indx] and indx in standard.lockls:
            standard.lockls.remove(indx)

    return {
        "time": base.show_time(),
        "devs": diskdict,
        "jobs": joblst,
    }


def work() -> None:
    main.run(
        host="0.0.0.0",  # noqa : S104
        port=standard.port,
        debug=standard.repair
    )
