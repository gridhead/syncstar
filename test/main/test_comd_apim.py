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

import pytest

from syncstar.config import apim_config, standard


@pytest.mark.parametrize(
    "_",
    [
        pytest.param(
            None,
            id="MAIN Function - APIM Command - Configuration"
        )
    ]
)
def test_comd_apim(_, mocker):
    # Foundation
    backup_port, backup_username, backup_password = standard.port, standard.username, standard.password
    port, username, password = 8484, urandom(8).hex().upper(), urandom(8).hex().upper()

    # Initialization
    apim_config(port, username, password)

    # Confirmation
    assert port == standard.port
    assert username == standard.username
    assert password == standard.password

    # Teardown
    standard.port, standard.username, standard.password = backup_port, backup_username, backup_password
