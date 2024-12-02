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
from syncstar.main import meet_apim


@pytest.mark.parametrize(
    "username, password, repair, output",
    [
        pytest.param(
            standard.username,
            standard.password,
            standard.repair,
            [
                f"Authentication username. '{standard.username}'",
                f"Authentication username. '{standard.password}'",
                f"Debug mode is {'enabled' if standard.repair else 'disabled'}",
            ],
            id="MEET_APIM Function - Standard parameters"
        ),
        pytest.param(
            "ABCD1234",
            "ABCD1234",
            True,
            [
                "Authentication username. 'ABCD1234'",
                "Authentication username. 'ABCD1234'",
                "Debug mode is enabled",
            ],
            id="MEET_APIM Function - Modified parameters"
        ),
    ]
)
def test_meet_apim(caplog, mocker, username, password, repair, output):
    # Initialization
    mocker.patch("syncstar.config.standard.username", username)
    mocker.patch("syncstar.config.standard.password", password)
    mocker.patch("syncstar.config.standard.repair", repair)

    # Confirmation
    meet_apim()
    for indx in output:
        assert indx in caplog.text
