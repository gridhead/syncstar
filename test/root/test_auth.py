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


@pytest.mark.parametrize(
    "code, text, word",
    [
        pytest.param(
            403,
            ["403", "Forbidden"],
            "CODEZEROEXISTENT",
            id="AUTH Middleware - 403 Unauthorized",
        ),
        pytest.param(
            200,
            ["devs", "jobs"],
            standard.code,
            id="AUTH Middleware - 200 OK",
        )
    ]
)
def test_auth(client, code, text, word):
    response = client.get(f"/read/{word}")
    assert response.status_code == code
    for indx in text:
        assert indx in response.data.decode()
