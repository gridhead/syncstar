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

from syncstar.config import cell_config, standard


@pytest.mark.parametrize(
    "_",
    [
        pytest.param(
            None,
            id="MAIN Function - CELL Command - Configuration"
        )
    ]
)
def test_comd_cell(_):
    # Foundation
    backup_proc, backup_compct = standard.proc, standard.compct
    subval_proc, subval_compct = 8, 8

    # Initialization
    cell_config(subval_proc, subval_compct)

    # Confirmation
    assert standard.proc == subval_proc
    assert standard.compct == subval_compct

    # Teardown
    standard.proc, standard.compct = backup_proc, backup_compct
