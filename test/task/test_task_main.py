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

from . import MockProcess, disklist_negative, disklist_positive, imdict, mock_update_state


@pytest.mark.parametrize(
    "work",
    [
        pytest.param(
            True,
            id="TASK Function - Task works positively"
        ),
        pytest.param(
            False,
            id="TASK Function - Task works negatively"
        )
    ]
)
def test_task_main(caplog, mocker, work):
    # Foundation
    backup_imdict, backup_plug, backup_tote = standard.imdict, standard.plug, standard.tote

    # Initialization
    standard.imdict = imdict
    mocker.patch("celery.Task.update_state", return_value=mock_update_state)
    mocker.patch("subprocess.Popen", return_value=MockProcess())

    # Confirmation
    if work:
        mocker.patch("syncstar.base.list_drives", disklist_positive)
        objc = wrap_diskdrop("AAAAAAAA", "AAAAAAAA")
        assert "Please remove the storage device and attempt booting from it" in caplog.text
        assert objc["time"]["stop"] - objc["time"]["strt"] >= 4
    else:
        mocker.patch("syncstar.base.list_drives", disklist_negative)
        with pytest.raises(Ignore):
            objc = wrap_diskdrop("AAAAAAAA", "AAAAAAAA")
            assert "Unsafe removal of storage device can cause hardware damage" in caplog.text
            assert objc is None

    # Teardown
    standard.imdict, standard.plug, standard.tote = backup_imdict, backup_plug, backup_tote
