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


from logging import getLogger
from logging.config import dictConfig

repair = False

port = 8080

period = 2

proc = 8

compct = 8

images = ""

imdict = {}

dkdict = {}

hsdict = {}

joblst = {}

lockls = []

code = "0000000000000000"

source = "redis://localhost:6379/0"
broker_link = source
result_link = source

# Variables used for the testing purposes

plug = 0

tote = 2

# Default configuration for service logging

logrconf = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s %(message)s",
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"],
    },
}

dictConfig(logrconf)

logger = getLogger(__name__)
