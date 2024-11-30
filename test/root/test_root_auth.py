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

import pytest

from syncstar.config import standard


@pytest.mark.parametrize(
    "code, text, username, password",
    [
        pytest.param(
            401,
            "NOPE",
            "CODEZEROEXISTENT",
            "CODEZEROEXISTENT",
            id="AUTH Middleware - 403 Unauthorized",
        ),
        pytest.param(
            200,
            "AJAO",
            standard.username,
            standard.password,
            id="AUTH Middleware - 200 OK",
        )
    ]
)
def test_auth(client, mocker, code, text, username, password):
    # Initialization
    mocker.patch("syncstar.config.standard.username", standard.username)
    mocker.patch("syncstar.config.standard.password", standard.password)

    # Confirmation
    head = {"username": username, "password": password}
    response = client.post("/sign", headers=head)
    assert response.status_code == code
    assert loads(response.data.decode())["data"] == text

    # Teardown
    response = client.post("/exit")
    assert response.status_code == code
