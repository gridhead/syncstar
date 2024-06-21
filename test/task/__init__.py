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


from syncstar.config import standard


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


class MockCompletionConfirmation:
    def __init__(self):
        self.qant = [8 for _ in range(standard.compct)]

    def __bool__(self):
        return True

    def push(self, item: int) -> None:
        return None


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


imdict = {
    "AAAAAAAA": {
        "name": "AAAAAAAA",
        "path": "/usr/bin/python",
        "size": 0
    }
}


def mock_update_state():
    return True


def disklist_positive():
    return diskdict


def disklist_negative():
    if standard.plug < standard.tote:
        standard.plug += 1
        return diskdict
    else:
        standard.plug = 0
        return {}
