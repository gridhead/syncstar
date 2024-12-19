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

from flask import Blueprint, Response, abort, jsonify, render_template, request, session

from syncstar import base, task
from syncstar.auth import checkpoint
from syncstar.config import standard
from syncstar.feed import create_result

root = Blueprint("root", __name__)


@root.route("/", methods=["GET"])
def home() -> str:
    """
    Handles the `/` endpoint to navigate the users to the application landing page

    :return: HTTP response
    """
    return render_template("home.html")


@root.route("/sign", methods=["POST"])
def sign() -> tuple[Response, int]:
    """
    Handles the `/sign` endpoint to create relevant session and provide a response

    :return: HTTP response
    """
    username, password = request.headers.get("username"), request.headers.get("password")
    if username == standard.username and password == standard.password:
        session["username"], session["password"] = username, password
        return jsonify({"data": "AJAO"}), 200
    return jsonify({"data": "NOPE"}), 401


@root.route("/sync/<diskindx>/<isosindx>", methods=["POST"])
@checkpoint
def sync(diskindx: str, isosindx: str) -> dict | Response:
    """
    Handles the `/sync` endpoint to request device creation and provide a response

    :return: HTTP response
    """
    iterdict = base.list_drives()

    if diskindx not in iterdict:
        abort(404, f"No such disk: {diskindx}")

    if isosindx not in standard.imdict:
        abort(404, f"No such image: {isosindx}")

    if diskindx in standard.lockls:
        abort(400, f"Disk locked: {diskindx}")

    if standard.imdict[isosindx]["size"] >= iterdict[diskindx]["size"]:
        abort(422, "Insufficient capacity")

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
        "rate": "0.00 B/s",
    }
    standard.lockls.append(diskindx)
    return {"location": unit.id}, 201


@root.route("/news", methods=["GET"])
@checkpoint
def news() -> dict:
    """
    Handles the `/news` endpoint to fetch all relevant feed and provide a response

    :return: HTTP response
    """
    return create_result()


@root.route("/read", methods=["GET"])
@checkpoint
def read() -> dict:
    """
    Handles the `/read` endpoint to fetch all relevant data and provide a response

    :return: HTTP response
    """
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
            joblst[indx]["rate"] = "0.00 B/s"
            if data["disk"] in standard.lockls:
                tounlock[data["disk"]] = False
        elif unit.state == "FAILURE":
            # Conditions - FAILURE
            joblst[indx]["time"] = data["time"]["stop"] - data["time"]["strt"]
            joblst[indx]["done"] = False
            joblst[indx]["rate"] = data["rate"]
            if data["disk"] in standard.lockls:
                tounlock[data["disk"]] = True
        else:
            # Conditions - SUCCESS and WORKING
            joblst[indx]["time"] = unit.info.get("time").get("stop", 0) - data["time"]["strt"]
            joblst[indx]["done"] = unit.info.get("finished", True)
            joblst[indx]["rate"] = unit.info.get("rate", "0.00 B/s")
            standard.joblst[indx]["rate"] = unit.info.get("rate", "0.00 B/s")
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
        "file": standard.imdict,
        "feed": standard.fdlist,
        "devs": diskdict,
        "jobs": joblst,
    }


@root.route("/exit", methods=["POST"])
@checkpoint
def exit() -> tuple[Response, int]:
    """
    Handles the `/exit` endpoint to clear the user session and provide a response

    :return: HTTP response
    """
    session.clear()
    return jsonify({"data": "OKAY"}), 200
