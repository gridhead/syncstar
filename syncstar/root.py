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
from syncstar import task

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
                    unit = task.sync_drives.apply_async(args=[diskindx, isosindx])
                    standard.joblst[iden] = {
                        "disk": diskindx,
                        "isos": isosindx,
                        "time": {
                            "strt": time(),
                            "stop": 0,
                        },
                        "task": unit.id
                    }
                    standard.lockls.append(diskindx)
                    return {
                        "location": unit.id,
                    }
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

    # Populate a dictionary of all the storage devices regardless of
    # they are connected currently or were connected in the past
    for jndx in diskdict:
        standard.hsdict[jndx] = diskdict[jndx]

    tounlock = {}

    for indx in standard.joblst.keys():
        data = standard.joblst[indx]
        unit = task.sync_drives.AsyncResult(str(data["task"]).encode())
        if unit.state == "PENDING":
            # Conditions - PENDING
            joblst[indx] = {
                "disk": f"{standard.hsdict[data['disk']]['name']['vendor']} {standard.hsdict[data['disk']]['name']['handle']}",
                "isos": standard.imdict[data["isos"]]["name"],
                "time": 0,
                "mood": unit.state,
                "done": False,
                "perc": 0
            }
        elif unit.state == "FAILURE":
            # Conditions - FAILURE
            joblst[indx] = {
                "disk": f"{standard.hsdict[data['disk']]['name']['vendor']} {standard.hsdict[data['disk']]['name']['handle']}",
                "isos": standard.imdict[data["isos"]]["name"],
                "time": 0,
                "mood": unit.state,
                "done": False,
                "perc": 0
            }
            if data["disk"] in standard.lockls:
                if unit.state == "FAILURE":
                    tounlock[data["disk"]] = True
        else:
            # Conditions - SUCCESS and WORKING
            joblst[indx] = {
                "disk": f"{standard.hsdict[data['disk']]['name']['vendor']} {standard.hsdict[data['disk']]['name']['handle']}",
                "isos": standard.imdict[data["isos"]]["name"],
                "time": unit.info.get("time").get("stop", 0) - unit.info.get("time").get("strt", 0),
                "mood": unit.state,
                "done": unit.info.get("finished", True),
                "perc": unit.info.get("progress", 100)
            }
            if data["disk"] in standard.lockls:
                if unit.state == "SUCCESS":
                    tounlock[data["disk"]] = True
                elif unit.state == "WORKING":
                    tounlock[data["disk"]] = False

    # Set flags for whenever the operational storage devices are removed during synchronization
    for indx in tounlock.keys():
        if tounlock[indx] and indx in standard.lockls:
            standard.lockls.remove(indx)

    return {
        "time": show_time(),
        "devs": diskdict,
        "jobs": joblst,
    }


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
