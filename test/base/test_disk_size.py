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


import subprocess

import pytest

from syncstar.base import retrieve_disk_size


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
    # Initialization & Confirmation
    if work:
        output = b"1024\n512\n256\n128\n128"
        mocker.patch("subprocess.check_output", return_value=output)
        assert retrieve_disk_size("/dev/null") == 1024
    else:
        mocker.patch("syncstar.base.retrieve_disk_size", side_effect=subprocess.CalledProcessError)
        assert retrieve_disk_size("/dev/null") == 0
