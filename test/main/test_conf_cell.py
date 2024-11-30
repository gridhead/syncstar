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
from click.testing import CliRunner

from syncstar.main import main


@pytest.mark.parametrize(
    "cmdl, code, text",
    [
        pytest.param(
            "--images /etc/ --source redis://localhost:6379/0 --repair true cell --proc 0 --poll 8",
            2,
            [
                "Usage: syncstar cell [OPTIONS]",
                "Try 'syncstar cell --help' for help.",
                "Error: Invalid value for '-p' / '--proc': 0 is not in the range 4<=x<=20.",
            ],
            id="MAIN Function - CELL Command - Incorrect input - PROC"
        ),
        pytest.param(
            "--images /etc/ --source redis://localhost:6379/0 --repair true cell --proc 8 --poll 0",
            2,
            [
                "Usage: syncstar cell [OPTIONS]",
                "Try 'syncstar cell --help' for help.",
                "Error: Invalid value for '-c' / '--poll': 0 is not in the range 4<=x<=12.",
            ],
            id="MAIN Function - CELL Command - Incorrect input - POLL"
        ),
    ]
)
def test_apim(mocker, cmdl, code, text):
    # Initialization
    mocker.patch("syncstar.config.main_config", return_value=True)
    runner = CliRunner()
    result = runner.invoke(main, cmdl)

    # Confirmation
    assert result.exit_code == code
    for indx in text:
        assert indx in result.output
