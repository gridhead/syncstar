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


import pytest

from syncstar.config import standard

from . import MockTaskResult


@pytest.mark.parametrize(
    "code, item, isos, objc, size, lock, text",
    [
        pytest.param(
            201,
            "ABCD1234",
            "ABCD1234",
            MockTaskResult(id="ABCD1234"),
            True,
            [],
            ["location", "ABCD1234"],
            id="KICK Endpoint - 201 Created",
        ),
        pytest.param(
            400,
            "ABCD1234",
            "ABCD1234",
            MockTaskResult(id="ABCD1234"),
            True,
            ["ABCD1234"],
            ["Bad", "Request", "Disk", "locked"],
            id="KICK Endpoint - 400 Bad Request - Disk locked",
        ),
        pytest.param(
            422,
            "ABCD1234",
            "ABCD1234",
            MockTaskResult(id="ABCD1234"),
            False,
            [],
            ["Unprocessable", "Entity", "Insufficient", "capacity"],
            id="KICK Endpoint - 422 Unprocessable Entity - Insufficient capacity",
        ),
        pytest.param(
            404,
            "CODEZERO",
            "ABCD1234",
            MockTaskResult(id="ABCD1234"),
            True,
            [],
            ["Not", "Found", "such", "disk"],
            id="KICK Endpoint - 404 Not Found - Disk unavailable",
        ),
        pytest.param(
            404,
            "ABCD1234",
            "CODEZERO",
            MockTaskResult(id="ABCD1234"),
            True,
            [],
            ["Not", "Found", "such", "image"],
            id="KICK Endpoint - 404 Not Found - Image unavailable",
        )
    ]
)
def test_sync(client, mocker, code, item, isos, objc, size, lock, text):
    # Initialization
    mocker.patch(
        "syncstar.config.standard.imdict",
        {
            "ABCD1234": {
                "path": "ABCD1234",
                "name": "ABCD1234",
                "type": "ABCD1234",
                "size": 0 if size else 2**40,
            }
        }
    )

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

    mocker.patch("syncstar.config.standard.lockls", lock)
    mocker.patch("syncstar.task.wrap_diskdrop.apply_async", return_value=objc)

    mocker.patch("syncstar.config.standard.username", "username")
    mocker.patch("syncstar.config.standard.password", "password")

    head = {"username": standard.username, "password": standard.password}
    response = client.post("/sign", headers=head)
    assert response.status_code == 200

    # Confirmation
    response = client.post(f"/sync/{item}/{isos}")
    assert response.status_code == code
    for indx in text:
        assert indx in response.data.decode()

    # Teardown
    response = client.post("/exit")
    assert response.status_code == 200
