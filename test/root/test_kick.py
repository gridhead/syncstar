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

import pytest

from syncstar.config import standard

from . import MockTaskResult


@pytest.mark.parametrize(
    "code, item, isos, objc, size, lock, text",
    [
        pytest.param(
            200,
            "AAAAAAAA",
            "AAAAAAAA",
            MockTaskResult(id="AAAAAAAA"),
            True,
            [],
            ["location", "AAAAAAAA"],
            id="KICK Endpoint - 200 OK",
        ),
        pytest.param(
            400,
            "AAAAAAAA",
            "AAAAAAAA",
            MockTaskResult(id="AAAAAAAA"),
            True,
            ["AAAAAAAA"],
            ["Bad", "Request", "Disk", "locked"],
            id="KICK Endpoint - 400 Bad Request - Disk locked",
        ),
        pytest.param(
            422,
            "AAAAAAAA",
            "AAAAAAAA",
            MockTaskResult(id="AAAAAAAA"),
            False,
            [],
            ["Unprocessable", "Entity", "Insufficient", "capacity"],
            id="KICK Endpoint - 422 Unprocessable Entity - Insufficient capacity",
        ),
        pytest.param(
            404,
            "CODEZERO",
            "AAAAAAAA",
            MockTaskResult(id="AAAAAAAA"),
            True,
            [],
            ["Not", "Found", "such", "disk"],
            id="KICK Endpoint - 404 Not Found - Disk unavailable",
        ),
        pytest.param(
            404,
            "AAAAAAAA",
            "CODEZERO",
            MockTaskResult(id="AAAAAAAA"),
            True,
            [],
            ["Not", "Found", "such", "image"],
            id="KICK Endpoint - 404 Not Found - Image unavailable",
        )
    ]
)
def test_kick(client, mocker, code, item, isos, objc, size, lock, text):
    # Foundation
    backup_imdict, backup_lockls = standard.imdict, standard.lockls

    # Initialization
    standard.imdict = {
        "AAAAAAAA": {
            "path": "AAAAAAAA",
            "name": "AAAAAAAA",
            "type": "AAAAAAAA",
            "size": 0 if size else 2**40,
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
    standard.lockls = lock
    mocker.patch("syncstar.base.list_drives", return_value=disk)
    mocker.patch("syncstar.task.wrap_diskdrop.apply_async", return_value=objc)
    response = client.get(f"/kick/{standard.code}/{item}/{isos}")

    # Confirmation
    assert response.status_code == code
    for indx in text:
        assert indx in response.data.decode()

    # Teardown
    standard.imdict, standard.lockls = backup_imdict, backup_lockls
