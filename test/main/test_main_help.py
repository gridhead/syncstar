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
            "--images /etc/ --source redis://localhost:6379/0 --repair true apim --help",
            0,
            [
                "Usage: syncstar apim [OPTIONS]",
                "Start the frontend service",
                "Options:",
                "-p, --port INTEGER RANGE",
                "-u, --username TEXT",
                "-w, --password TEXT",
                "--help",
                "Set the port value for the service frontend",
                "endpoints.  [default: 8080; 64<=x<=65535]",
                "Set the username for service authentication.",
                "[default: root]",
                "Set the password for service authentication.",
                "[default: root]",
                "Show this message and exit."
            ],
            id="MAIN Function - APIM - Basic help"
        ),
        pytest.param(
            "--images /etc/ --source redis://localhost:6379/0 --repair true cell --help",
            0,
            [
                "Usage: syncstar cell [OPTIONS]",
                "Start the worker service",
                "Options:",
                "-p, --proc INTEGER RANGE",
                "-c, --poll INTEGER RANGE",
                "--help",
                "Set the number of concurrent worker tasks allowed.",
                "[default: 8; 4<=x<=20]",
                "Set the number of completion checks for termination.",
                "[default: 8; 4<=x<=12]",
                "Show this message and exit.",
            ],
            id="MAIN Function - CELL - Basic help"
        )
    ]
)
def test_help(mocker, cmdl, code, text):
    # Initialization
    mocker.patch("syncstar.config.main_config", return_value=True)
    runner = CliRunner()
    result = runner.invoke(main, cmdl)

    # Confirmation
    assert result.exit_code == code
    for indx in text:
        assert indx in result.output
