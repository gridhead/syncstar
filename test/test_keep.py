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

from syncstar.config import keep_config, standard


@pytest.mark.parametrize(
    "port, repair, period, severity",
    [
        pytest.param(
            standard.port,
            standard.repair,
            standard.period,
            "INFO",
            id="KEEPCONFIG Function - Standard configuration",
        ),
        pytest.param(
            9090,
            True,
            10,
            "DEBUG",
            id="KEEPCONFIG Function - Modified configuration",
        )
    ]
)
def test_keep(port, repair, period, severity):
    # Foundation
    backup_port, backup_repair, backup_period, backup_logrconf = standard.port, standard.repair, standard.period, standard.logrconf

    # Initialization
    keep_config(port, repair, period)

    # Confirmation
    assert standard.port == port
    assert standard.repair == repair
    assert standard.period == period
    assert standard.logrconf["handlers"]["console"]["level"] == severity
    assert standard.logrconf["root"]["level"] == severity

    # Teardown
    standard.port, standard.repair, standard.period, standard.logrconf = backup_port, backup_repair, backup_period, backup_logrconf
