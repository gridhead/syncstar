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
            "--images /etc/ --source redis://localhost:6379/0 --repair true apim --port 0 --username username --password password",
            2,
            [
                "Usage: syncstar apim [OPTIONS]",
                "Try 'syncstar apim --help' for help.",
                "Error: Invalid value for '-p' / '--port': 0 is not in the range 64<=x<=65535.",
            ],
            id="MAIN Function - APIM Command - Incorrect input - PORT"
        ),
        pytest.param(
            "--images /etc/ --source redis://localhost:6379/0 --repair true apim --port 8080 --username",
            2,
            [
                "Error: Option '--username' requires an argument.",
            ],
            id="MAIN Function - APIM Command - Incorrect input - USERNAME"
        ),
        pytest.param(
            "--images /etc/ --source redis://localhost:6379/0 --repair true apim --port 8080 --password",
            2,
            [
                "Error: Option '--password' requires an argument.",
            ],
            id="MAIN Function - APIM Command - Incorrect input - PASSWORD"
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
