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

from syncstar import __versdata__
from syncstar.main import main


@pytest.mark.parametrize(
    "cmdl, code, text",
    [
        pytest.param(
            "--help",
            0,
            [
                "Usage: syncstar [OPTIONS] COMMAND [ARGS]...",
                "Options:",
                "-i, --images PATH",
                "-s, --source PATH",
                "-r, --repair BOOLEAN",
                "--version",
                "--help",
                "Set the location to where the images config is stored",
                "[required]",
                "Set the location where tasks will be exchanged",
                "[default: redis://localhost:6379/0]",
                "Show the nerdy statistics to help repair the codebase",
                "[default: False]",
                "Show the version and exit.",
                "Show this message and exit.",
                "Commands:",
                "apim",
                "cell",
                "Start the frontend service",
                "Start the worker service",
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


@pytest.mark.parametrize(
    "cmdl, code, text",
    [
        pytest.param(
            "--images /etc/ --source redis://localhost:6379/0 --repair true apim --port 0 --period 2",
            2,
            [
                "Usage: syncstar apim [OPTIONS]",
                "Try 'syncstar apim --help' for help.",
                "Error: Invalid value for '-p' / '--port': 0 is not in the range 64<=x<=65535.",
            ],
            id="MAIN Function - Incorrect input - PORT"
        ),
        pytest.param(
            "--images /etc/ --source redis://localhost:6379/0 --repair true apim --port 8080 --period 0",
            2,
            [
                "Usage: syncstar apim [OPTIONS]",
                "Try 'syncstar apim --help' for help.",
                "Error: Invalid value for '-t' / '--period': 0 is not in the range 2<=x<=30.",
            ],
            id="MAIN Function - Incorrect input - PERIOD"
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


@pytest.mark.parametrize(
    "cmdl, code, text",
    [
        pytest.param(
            "--images /etc/zeroexistent",
            2,
            [
                "Usage: syncstar [OPTIONS] COMMAND [ARGS]...",
                "Try 'syncstar --help' for help.",
                "Error: Invalid value for '-i' / '--images': Path '/etc/zeroexistent' does not exist.",
            ],
            id="MAIN Function - Incorrect input - IMAGES"
        ),
        pytest.param(
            "--repair zeroexistent",
            2,
            [
                "Usage: syncstar [OPTIONS] COMMAND [ARGS]...",
                "Try 'syncstar --help' for help.",
                "Error: Invalid value for '-r' / '--repair': 'zeroexistent' is not a valid boolean."
            ],
            id="MAIN Function - Incorrect input - REPAIR"
        )
    ]
)
def test_main_conf(cmdl, code, text):
    # Initialization
    runner = CliRunner()
    result = runner.invoke(main, cmdl)

    # Confirmation
    assert result.exit_code == code
    for indx in text:
        assert indx in result.output


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
    ]
)
def test_main_comd(mocker, cmdl, code, text):
    # Initialization
    mocker.patch("syncstar.config.main_config", return_value=True)
    runner = CliRunner()
    result = runner.invoke(main, cmdl)

    # Confirmation
    assert result.exit_code == code
    for indx in text:
        assert indx in result.output
