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

from syncstar import __versdata__
from syncstar.config import standard
from syncstar.main import meet


@pytest.mark.parametrize(
    "code, period, repair, output",
    [
        pytest.param(
            standard.code,
            standard.period,
            standard.repair,
            [
                f"Starting SyncStar v{__versdata__}...",
                f"Use the secret code '{standard.code}' to authenticate with the service",
                f"Information on the frontend would be refreshed every after {standard.period} second(s)",
                f"Debug mode is {'enabled' if standard.repair else 'disabled'}",
            ],
            id="MEET Function - Standard parameters"
        ),
        pytest.param(
            "XXXXXXXXXXXXXXXX",
            10,
            True,
            [
                f"Starting SyncStar v{__versdata__}...",
                "Use the secret code 'XXXXXXXXXXXXXXXX' to authenticate with the service",
                "Information on the frontend would be refreshed every after 10 second(s)",
                "Debug mode is enabled",
            ],
            id="MEET Function - Modified parameters"
        ),
    ]
)
def test_meet(caplog, code, period, repair, output):
    standard.code, standard.period, standard.repair = code, period, repair
    meet()
    for indx in output:
        assert indx in caplog.text
