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


import subprocess
from hashlib import sha256

import pytest

from syncstar.base import list_drives, retrieve_disk_size
from syncstar.config import standard


class MockDeviceItem:
    def __init__(self, iden: str):
        self.ID_BUS = "usb"
        self.device_node = "/dev/null"
        self.device_number = "12121999"
        self.iden = iden
        self.size = 0
        self.properties = {
            "ID_SERIAL_SHORT": iden,
            "ID_VENDOR": iden,
            "ID_MODEL": iden,
        }

    def get(self, item: str):
        return self.ID_BUS


class MockDeviceList:
    def __init__(self, devs: list):
        self.devs = devs
        self.indx = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.indx < len(self.devs):
            item = self.devs[self.indx]
            self.indx += 1
            return item
        raise StopIteration


@pytest.mark.parametrize(
    "work",
    [
        pytest.param(
            True,
            id="DISKSIZE Function - Function works positively",
        ),
        pytest.param(
            False,
            id="DISKSIZE Function - Function works negatively",
        )
    ]
)
def test_disk_size(mocker, work):
    if work:
        output = b"1024\n512\n256\n128\n128"
        mocker.patch("subprocess.check_output", return_value=output)
        assert retrieve_disk_size("/dev/null") == 1024
    else:
        mocker.patch("syncstar.base.retrieve_disk_size", side_effect=subprocess.CalledProcessError)
        assert retrieve_disk_size("/dev/null") == 0


@pytest.mark.parametrize(
    "_",
    [
        pytest.param(
            None,
            id="LISTDRIVES Function - Function works positively"
        )
    ]
)
def test_list_drives(mocker, _):
    mocklist = MockDeviceList(
        [
            MockDeviceItem("AAAAAAAA"),
            MockDeviceItem("BBBBBBBB"),
            MockDeviceItem("CCCCCCCC"),
            MockDeviceItem("DDDDDDDD"),
        ]
    )
    mocker.patch("syncstar.base.retrieve_disk_size", return_value=0)
    mocker.patch("pyudev.Context.list_devices", return_value=mocklist)
    list_drives()
    for indx in mocklist:
        hash = sha256(indx.iden.encode()).hexdigest()[0:8].upper()
        assert hash in standard.dkdict
        assert indx.device_number == standard.dkdict[hash]["iden"]
        assert indx.size == standard.dkdict[hash]["size"]
        assert indx.properties["ID_VENDOR"] == standard.dkdict[hash]["name"]["vendor"]
        assert indx.properties["ID_HANDLE"] == standard.dkdict[hash]["name"]["handle"]
        assert indx.device_node == standard.dkdict[hash]["node"]
