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
def test_comd_apim(_):
    # Foundation
    backup_code, backup_port, backup_period = standard.code, standard.port, standard.period
    subval_code, subval_port, subval_period = "0000000000000000", 0, 0  # noqa: F841

    # Initialization
    apim_config(subval_port, subval_period)

    # Confirmation
    assert len(standard.code) == 16
    assert standard.port == subval_port
    assert standard.period == subval_period

    # Teardown
    standard.code, standard.port, standard.period = backup_code, backup_port, backup_period
