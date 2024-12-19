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
from celery.exceptions import Ignore

from syncstar.config import standard
from syncstar.task import wrap_diskdrop

from . import MockCompletionConfirmation, MockProcess, disklist_positive, imdict, mock_update_state


@pytest.mark.parametrize(
    "output",
    [
        pytest.param(
            "record",
            id="TASK Function - Long task complete - Record output"
        ),
        pytest.param(
            "copied",
            id="TASK Function - Long task complete - Copied output"
        ),
    ]
)
def test_task_long(caplog, mocker, output):
    # Initialization
    mocker.patch("syncstar.config.standard.imdict", imdict)
    mocker.patch("syncstar.util.CompletionConfirmation", MockCompletionConfirmation)
    mocker.patch("celery.Task.update_state", return_value=mock_update_state)
    mocker.patch("subprocess.Popen", return_value=MockProcess(output))
    mocker.patch("syncstar.base.list_drives", disklist_positive)

    # Confirmation
    with pytest.raises(Ignore):
        objc = wrap_diskdrop("AAAAAAAA", "AAAAAAAA")
        assert f"Long running task safely terminated after {standard.poll} checks" in caplog.text
        assert objc["time"]["stop"] - objc["time"]["strt"] >= 1
