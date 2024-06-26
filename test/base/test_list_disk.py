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


from hashlib import sha256

import pytest

from syncstar.base import list_drives
from syncstar.config import standard

from . import MockDeviceItem, MockDeviceList


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
    # Foundation
    backup_dkdict = standard.dkdict

    # Initialization
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

    # Confirmation
    for indx in mocklist:
        hash = sha256(indx.iden.encode()).hexdigest()[0:8].upper()
        assert hash in standard.dkdict
        assert indx.device_number == standard.dkdict[hash]["iden"]
        assert indx.size == standard.dkdict[hash]["size"]
        assert indx.properties["ID_VENDOR"] == standard.dkdict[hash]["name"]["vendor"]
        assert indx.properties["ID_HANDLE"] == standard.dkdict[hash]["name"]["handle"]
        assert indx.device_node == standard.dkdict[hash]["node"]

    # Teardown
    standard.dkdict = backup_dkdict
