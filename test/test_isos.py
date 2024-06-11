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

from os.path import abspath, realpath
from tempfile import TemporaryDirectory

import pytest

from syncstar.config import isos_config, standard


@pytest.mark.parametrize(
    "work, text",
    [
        pytest.param(
            0,
            [
                "Images configuration file not detected",
            ],
            id="ISOSCONFIG Function - Negative ISOSYAML configuration - Absent config"
        ),
        pytest.param(
            1,
            [
                "Invalid images configuration file detected - UnicodeDecodeError",
            ],
            id="ISOSCONFIG Function - Negative ISOSYAML configuration - Invalid config"
        ),
        pytest.param(
            2,
            [
                "Checking image file for 'AAAAAAAAAAAAAAAA'...",
            ],
            id="ISOSCONFIG Function - Positive ISOSYAML configuration - Images file present"
        ),
        pytest.param(
            3,
            [
                "Images file for 'AAAAAAAAAAAAAAAA' was not found",
            ],
            id="ISOSCONFIG Function - Negative ISOSYAML configuration - Images file not present",
        ),
        pytest.param(
            4,
            [
                "Empty images configuration file detected",
            ],
            id="ISOSCONFIG Function - Negative ISOSYAML configuration - Empty config",
        ),
    ]
)
def test_isos(caplog, work, text):
    # Foundation
    backup_images, backup_imdict = standard.images, standard.imdict

    # Initialization & Confirmation
    if work in [0, 1]:
        if work == 0:   temppath = "/usr/bin/zeroexistent"
        else:           temppath = "/usr/bin/python3"
        with pytest.raises(SystemExit) as func:
            isos_config(temppath)
            assert func.value.code == 1
    else:
        with TemporaryDirectory(prefix="syncstar-test-") as tempdrct:
            temppath = f"{tempdrct}/images.yml"
            yamlpath = abspath(realpath(__file__)).replace("test_isos.py", "data/images.yml")

            with open(yamlpath) as yamlfile:        yamldata = yamlfile.read()
            if work == 2:                           yamldata = yamldata.replace("LOCATION", temppath)
            elif work == 3:                         yamldata = yamldata.replace("LOCATION", "ZEROEXISTENT")
            elif work == 4:                         yamldata = "---"
            with open(temppath, "w") as yamlfile:   yamlfile.write(yamldata)

            if work != 2:
                with pytest.raises(SystemExit) as func:
                    isos_config(temppath)
                    assert func.value.code == 1
            else:
                isos_config(temppath)

    # Initialization & Confirmation
    for indx in text:
        assert indx in caplog.text

    # Teardown
    standard.images, standard.imdict = backup_images, backup_imdict
