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


from json import loads
from time import time

import pytest

from syncstar.config import standard

from . import MockAsyncResult


@pytest.mark.parametrize(
    "mood, objc, jobs",
    [
        pytest.param(
            "PENDING",
            MockAsyncResult(iden="AAAAAAAA", state="PENDING", info={"time": {"strt": time(), "stop": time()}, "finished": False, "progress": 0}),
            {"AAAAAAAA": {"disk": "AAAAAAAA", "isos": "AAAAAAAA", "time": {"strt": time(), "stop": time(), }, "task": "AAAAAAAA", "rcrd": 0}},
            id="READ Endpoint - Jobs listing - PENDING"
        ),
        pytest.param(
            "FAILURE",
            MockAsyncResult(iden="AAAAAAAA", state="FAILURE", info={"time": {"strt": time(), "stop": time()}, "finished": True, "progress": 0}),
            {"AAAAAAAA": {"disk": "AAAAAAAA", "isos": "AAAAAAAA", "time": {"strt": time(), "stop": time(), }, "task": "AAAAAAAA", "rcrd": 0}},
            id="READ Endpoint - Jobs listing - FAILURE"
        ),
        pytest.param(
            "SUCCESS",
            MockAsyncResult(iden="AAAAAAAA", state="SUCCESS", info={"time": {"strt": time(), "stop": time()}, "finished": True, "progress": 0}),
            {"AAAAAAAA": {"disk": "AAAAAAAA", "isos": "AAAAAAAA", "time": {"strt": time(), "stop": time(), }, "task": "AAAAAAAA", "rcrd": 0}},
            id="READ Endpoint - Jobs listing - SUCCESS"
        ),
        pytest.param(
            "WORKING",
            MockAsyncResult(iden="AAAAAAAA", state="WORKING", info={"time": {"strt": time(), "stop": time()}, "finished": False, "progress": 0}),
            {"AAAAAAAA": {"disk": "AAAAAAAA", "isos": "AAAAAAAA", "time": {"strt": time(), "stop": time(), }, "task": "AAAAAAAA", "rcrd": 0}},
            id="READ Endpoint - Jobs listing - WORKING"
        ),
    ]
)
def test_read(client, mocker, mood, objc, jobs):
    standard.joblst = jobs
    standard.imdict = {
        "AAAAAAAA": {
            "path": "AAAAAAAA",
            "name": "AAAAAAAA",
            "type": "AAAAAAAA",
            "size": 0,
        }
    }
    disk = {
        "AAAAAAAA": {
            "node": "/dev/null",
            "name": {
                "vendor": "AAAAAAAA",
                "handle": "AAAAAAAA"
            },
            "iden": 2048,
            "size": 2000682496
        }
    }
    standard.lockls = [
        "AAAAAAAA"
    ]
    mocker.patch("syncstar.base.list_drives", return_value=disk)
    mocker.patch("syncstar.task.wrap_diskdrop.AsyncResult", return_value=objc)
    response = client.get(f"/read/{standard.code}")
    assert loads(response.data.decode())["devs"] == disk
    assert response.status_code == 200
    assert standard.hsdict == disk
