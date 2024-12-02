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


from json import loads
from time import time

import pytest

from syncstar.config import standard

from . import MockAsyncResult


@pytest.mark.parametrize(
    "mood",
    [
        pytest.param(
            "PENDING",
            id="READ Endpoint - Jobs listing - PENDING"
        ),
        pytest.param(
            "FAILURE",
            id="READ Endpoint - Jobs listing - FAILURE"
        ),
        pytest.param(
            "SUCCESS",
            id="READ Endpoint - Jobs listing - SUCCESS"
        ),
        pytest.param(
            "WORKING",
            id="READ Endpoint - Jobs listing - WORKING"
        ),
    ]
)
def test_read(client, mocker, mood):
    # Initialization
    mocker.patch(
        "syncstar.config.standard.hsdict",
        {
            "ABCD1234": {
                "iden": 2048,
                "name": {
                    "handle": "ABCD1234",
                    "vendor": "ABCD1234"
                },
                "node": "/dev/null",
                "size": 2000682496
            }
        }
    )
    mocker.patch("syncstar.base.list_drives", return_value=standard.hsdict)

    mocker.patch(
        "syncstar.config.standard.imdict",
        {
            "ABCD1234": {
                "path": "ABCD1234",
                "name": "ABCD1234",
                "type": "ABCD1234",
                "size": 0,
            }
        }
    )

    period = time()
    mocker.patch(
        "syncstar.config.standard.joblst",
        {
            "ABCD1234": {
                "disk": "ABCD1234",
                "isos": "ABCD1234",
                "time": {
                    "strt": period,
                    "stop": period
                },
                "task": "ABCD1234",
                "rcrd": 0
            }
        }
    )

    mocker.patch("syncstar.task.wrap_diskdrop.AsyncResult",
        return_value=MockAsyncResult(
        iden="ABCD1234",
        state=mood,
        info={
            "time": {
                "strt": period,
                "stop": period
            },
            "finished": True if mood in ["SUCCESS", "FAILURE"] else False,
            "progress": 0
        }
    ))

    lockls = [
        "ABCD1234"
    ]
    mocker.patch("syncstar.config.standard.lockls", lockls)

    mocker.patch("syncstar.config.standard.username", "username")
    mocker.patch("syncstar.config.standard.password", "password")

    head = {"username": standard.username, "password": standard.password}
    response = client.post("/sign", headers=head)
    assert response.status_code == 200

    # Confirmation
    response = client.get("/read")
    assert response.status_code == 200
    assert loads(response.data.decode())["devs"] == standard.hsdict
    assert loads(response.data.decode())["file"] == standard.imdict
    assert loads(response.data.decode())["file"].keys() == standard.joblst.keys()

    # Teardown
    response = client.post("/exit")
    assert response.status_code == 200
