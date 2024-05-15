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


from click import command, option, version_option, IntRange

from syncstar import __versdata__

from syncstar.config import keep_config

from syncstar.page import work

from syncstar.config import standard

from syncstar import view


def meet() -> None:
    view.success(f"Welcome to SyncStar v{__versdata__}!")
    view.section(f"Use the secret code '{standard.code}' to authenticate with the service")


@command(name="syncstar")
@option(
    "-p",
    "--port",
    "port",
    type=IntRange(min=64, max=65535),
    default=8080,
    required=False,
    help="Set the port value for the service frontend [64-65536]"
)
@option(
    "-r",
    "--repair",
    "repair",
    type=bool,
    default=False,
    required=False,
    help="Show the nerdy statistics to help repair the codebase"
)
@version_option(
    version=__versdata__, prog_name="SyncStar by Akashdeep Dhar"
)
def main(port: int = 8080, repair: bool = False) -> None:
    keep_config(port, repair)
    meet()
    work()
