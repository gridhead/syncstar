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

from flask import Flask, render_template, abort

from syncstar.config import standard, manifest
from syncstar import __versdata__
from syncstar.auth import checkpoint
from syncstar.base import list_drives, show_time


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
                    standard.lockls.append(diskindx)
                    return {
                        "diskindx": diskindx,
                        "isosindx": isosindx,
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
    return {
        "time": show_time(),
        "devs": list_drives(),
    }


def work() -> None:
    main.run(
        host="0.0.0.0",
        port=standard.port,
        debug=standard.repair
    )
