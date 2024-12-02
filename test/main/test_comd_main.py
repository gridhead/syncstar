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
            "--images /etc/ --source redis://localhost:6379/0 --repair true",
            2,
            [
                "Usage: syncstar [OPTIONS] COMMAND [ARGS]...",
                "Try 'syncstar --help' for help.",
                "Error: Missing command.",
            ],
            id="MAIN Function - Missing command"
        ),
        pytest.param(
            "--images /etc/ --source redis://localhost:6379/0 --repair true zeroexistent",
            2,
            [
                "Usage: syncstar [OPTIONS] COMMAND [ARGS]...",
                "Try 'syncstar --help' for help.",
                "Error: No such command 'zeroexistent'.",
            ],
            id="MAIN Function - Invalid command"
        ),
        pytest.param(
            "--images zeroexistent --source redis://localhost:6379/0 --repair true apim",
            2,
            [
                "Usage: syncstar [OPTIONS] COMMAND [ARGS]...",
                "Try 'syncstar --help' for help.",
                "Error: Invalid value for '-i' / '--images': Path 'zeroexistent' does not exist.",
            ],
            id="MAIN Function - Invalid path"
        ),
        pytest.param(
            "--images",
            2,
            [
                "Error: Option '--images' requires an argument.",
            ],
            id="MAIN Function - Unavailable path"
        ),
        pytest.param(
            "--images /etc/ --source redis://localhost:6379/0 --repair yeah apim",
            2,
            [
                "Usage: syncstar [OPTIONS] COMMAND [ARGS]...",
                "Try 'syncstar --help' for help.",
                "Error: Invalid value for '-r' / '--repair': 'yeah' is not a valid boolean.",
            ],
            id="MAIN Function - Invalid repair"
        ),
        pytest.param(
            "--repair",
            2,
            [
                "Error: Option '--repair' requires an argument.",
            ],
            id="MAIN Function - Unavailable repair"
        ),
        pytest.param(
            "--source",
            2,
            [
                "Error: Option '--source' requires an argument.",
            ],
            id="MAIN Function - Unavailable exchange"
        ),
    ]
)
def test_comd_main(mocker, cmdl, code, text):
    # Initialization
    mocker.patch("syncstar.config.main_config", return_value=True)
    runner = CliRunner()
    result = runner.invoke(main, cmdl)

    # Confirmation
    assert result.exit_code == code
    for indx in text:
        assert indx in result.output
