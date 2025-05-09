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


from click import style

from syncstar.config import standard


def success(message) -> None:
    """
    Log the message in the "SUCCESS" format

    :return:
    """
    standard.logger.info(style(message, fg="green", bold=True))


def failure(message) -> None:
    """
    Log the message in the "FAILURE" format

    :return:
    """
    standard.logger.error(style(message, fg="red", bold=True))


def warning(message) -> None:
    """
    Log the message in the "WARNING" format

    :return:
    """
    standard.logger.warning(style(message, fg="yellow", bold=True))


def general(message) -> None:
    """
    Log the message in the "GENERAL" format

    :return:
    """
    standard.logger.info(message)
