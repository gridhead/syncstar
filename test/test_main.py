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
from click.testing import CliRunner

from syncstar import __versdata__
from syncstar.main import main


@pytest.mark.parametrize(
    "cmdl, code, text",
    [
        pytest.param(
            "--help",
            0,
            [
                "Usage: syncstar [OPTIONS]",
                "Options:",
                "-p, --port INTEGER RANGE",
                "-r, --repair BOOLEAN",
                "-t, --period INTEGER RANGE",
                "-i, --images PATH",
                "--version",
                "--help",
                "Set the port value for the service frontend",
                "endpoints  [64<=x<=65535]",
                "Show the nerdy statistics to help repair the",
                "codebase",
                "Set the period after which the info will be",
                "refreshed  [2<=x<=30]",
                "Set the location to where the images config is",
                "stored  [required]",
                "Show the version and exit.",
                "Show this message and exit.",
            ],
            id="MAIN Function - Basic help"
        ),
        pytest.param(
            "--version",
            0,
            [
                f"SyncStar by Akashdeep Dhar, version {__versdata__}",
            ],
            id="MAIN Function - Version information"
        ),
        pytest.param(
            "--port 0 --repair true --period 2 --images /etc/",
            2,
            [
                "Usage: syncstar [OPTIONS]",
                "Try 'syncstar --help' for help.",
                "Error: Invalid value for '-p' / '--port': 0 is not in the range 64<=x<=65535.",
            ],
            id="MAIN Function - Incorrect input - PORT"
        ),
        pytest.param(
            "--port 8080 --repair medium --period 2 --images /etc/",
            2,
            [
                "Usage: syncstar [OPTIONS]",
                "Try 'syncstar --help' for help.",
                "Error: Invalid value for '-r' / '--repair': 'medium' is not a valid boolean.",
            ],
            id="MAIN Function - Incorrect input - REPAIR"
        ),
        pytest.param(
            "--port 8080 --repair true --period 0 --images /etc/",
            2,
            [
                "Usage: syncstar [OPTIONS]",
                "Try 'syncstar --help' for help.",
                "Error: Invalid value for '-t' / '--period': 0 is not in the range 2<=x<=30.",
            ],
            id="MAIN Function - Incorrect input - PERIOD"
        ),
        pytest.param(
            "--port 8080 --repair true --period 2 --images /etc/zeroexistent",
            2,
            [
                "Usage: syncstar [OPTIONS]",
                "Try 'syncstar --help' for help.",
                "Error: Invalid value for '-i' / '--images': Path '/etc/zeroexistent' does not exist.",
            ],
            id="MAIN Function - Incorrect input - IMAGES"
        ),
    ]
)
def test_main(cmdl, code, text):
    # Initialization
    runner = CliRunner()
    result = runner.invoke(main, cmdl)

    # Confirmation
    assert result.exit_code == code
    for indx in text:
        assert indx in result.output
