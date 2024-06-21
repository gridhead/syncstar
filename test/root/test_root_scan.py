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


@pytest.mark.parametrize(
    "code, text, lock, size, item",
    [
        pytest.param(200, [], [], True, "AAAAAAAA", id="SCAN Endpoint - 200 OK - Positive fit"),
        pytest.param(200, [], [], False, "AAAAAAAA", id="SCAN Endpoint - 200 OK - Negative fit"),
        pytest.param(404, [], [], True, "CODEZERO", id="SCAN Endpoint - 404 Not Found"),
        pytest.param(400, [], ["AAAAAAAA"], False, "AAAAAAAA", id="SCAN Endpoint - 400 Bad Request"),
    ]
)
def test_scan(client, mocker, code, text, lock, size, item):
    # Foundation
    backup_imdict, backup_dkdict, backup_lock = standard.imdict, standard.dkdict, standard.lockls

    # Initialization
    standard.imdict = {
        "AAAAAAAA": {
            "path": "AAAAAAAA",
            "name": "AAAAAAAA",
            "type": "AAAAAAAA",
            "size": 0 if size else 2**40,
        }
    }
    standard.dkdict = {
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
    mocker.patch("syncstar.base.list_drives", return_value=standard.dkdict)
    response = client.get(f"/scan/{standard.code}/{item}")

    # Confirmation
    assert response.status_code == code
    for indx in text:
        assert indx in response.data.decode()

    # Teardown
    standard.imdict, standard.dkdict, standard.lockls = backup_dkdict, backup_imdict, backup_lock
