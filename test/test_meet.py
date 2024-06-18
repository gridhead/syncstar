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

from syncstar.config import standard
from syncstar.main import meet_apim, meet_cell


@pytest.mark.parametrize(
    "code, period, repair, output",
    [
        pytest.param(
            standard.code,
            standard.period,
            standard.repair,
            [
                f"Use the secret code '{standard.code}' to authenticate with the service",
                f"Information on the frontend would be refreshed every after {standard.period} second(s)",
                f"Debug mode is {'enabled' if standard.repair else 'disabled'}",
            ],
            id="MEET_APIM Function - Standard parameters"
        ),
        pytest.param(
            "XXXXXXXXXXXXXXXX",
            10,
            True,
            [
                "Use the secret code 'XXXXXXXXXXXXXXXX' to authenticate with the service",
                "Information on the frontend would be refreshed every after 10 second(s)",
                "Debug mode is enabled",
            ],
            id="MEET_APIM Function - Modified parameters"
        ),
    ]
)
def test_meet_apim(caplog, code, period, repair, output):
    # Foundation
    backup_code, backup_period, backup_repair = standard.code, standard.period, standard.repair

    # Initialization
    standard.code, standard.period, standard.repair = code, period, repair
    meet_apim()

    # Confirmation
    for indx in output:
        assert indx in caplog.text

    # Teardown
    standard.code, standard.period, standard.repair = backup_code, backup_period, backup_repair


@pytest.mark.parametrize(
    "images, source, output",
    [
        pytest.param(
            standard.images,
            standard.source,
            [
                f"Images config - '{standard.images}'",
                f"Broker source - '{standard.broker_link}'",
                f"Result source - '{standard.result_link}'",
            ],
            id="MEET_CELL Function - Standard parameters"
        ),
        pytest.param(
            "/etc/zeroexistent",
            "/etc/zeroexistent",
            [
                "Images config - '/etc/zeroexistent'",
                "Broker source - '/etc/zeroexistent'",
                "Result source - '/etc/zeroexistent'",
            ],
            id="MEET_CELL Function - Modified parameters"
        ),
    ]
)
def test_meet_cell(caplog, images, source, output):
    # Foundation
    backup_images, backup_source = standard.images, standard.source

    # Initialization
    standard.images = images
    standard.broker_link, standard.result_link = source, source
    meet_cell()

    # Confirmation
    for indx in output:
        assert indx in caplog.text

    # Teardown
    standard.images, standard.source = backup_images, backup_source
    standard.broker_link, standard.result_link = backup_source, backup_source
