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
from celery.exceptions import Ignore

from syncstar.config import standard
from syncstar.task import wrap_diskdrop


class MockStandardError:
    def __init__(self):
        pass

    def readline(self):
        return b"0 records out"


class MockProcess:
    def __init__(self):
        self.border = 4
        self.indx = 0
        self.stderr = MockStandardError()

    def send_signal(self, data):
        return True

    def poll(self):
        if self.indx < self.border:
            self.indx += 1
            return None
        else:
            return True


def mock_update_state():
    return True


diskdict = {
    "AAAAAAAA": {
        "node": "/dev/null",
        "name": {
            "vendor": "AAAAAAAA",
            "handle": "AAAAAAAA"
        },
        "iden": 2048,
        "size": 2000682496
    }
}


def disklist_positive():
    return diskdict


def disklist_negative():
    if standard.plug < standard.tote:
        standard.plug += 1
        return diskdict
    else:
        standard.plug = 0
        return {}


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
def test_task(mocker, work):
    standard.imdict = {
        "AAAAAAAA": {
            "name": "AAAAAAAA",
            "path": "/usr/bin/python",
            "size": 0
        }
    }

    mocker.patch("celery.Task.update_state", return_value=mock_update_state)
    mocker.patch("syncstar.config.isos_config", return_value=True)
    mocker.patch("subprocess.Popen", return_value=MockProcess())

    if work:
        mocker.patch("syncstar.base.list_drives", disklist_positive)
        objc = wrap_diskdrop("AAAAAAAA", "AAAAAAAA")
        assert objc["time"]["stop"] - objc["time"]["strt"] >= 4
    else:
        mocker.patch("syncstar.base.list_drives", disklist_negative)
        with pytest.raises(Ignore):
            objc = wrap_diskdrop("AAAAAAAA", "AAAAAAAA")
            assert objc is None
