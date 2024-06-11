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


from click import IntRange, Path, command, option, version_option

from syncstar import __versdata__, view
from syncstar.config import isos_config, keep_config, standard
from syncstar.root import work


def meet() -> None:
    view.success(
        f"Starting SyncStar v{__versdata__}..."
    )
    view.warning(
        f"Use the secret code '{standard.code}' to authenticate with the service"
    )
    view.warning(
        f"Information on the frontend would be refreshed every after {standard.period} second(s)"
    )
    view.warning(
        f"Debug mode is {'enabled' if standard.repair else 'disabled'}"
    )


@command(name="syncstar")
@option(
    "-p",
    "--port",
    "port",
    type=IntRange(min=64, max=65535),
    default=8080,
    required=False,
    help="Set the port value for the service frontend endpoints"
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
@option(
    "-t",
    "--period",
    "period",
    type=IntRange(min=2, max=30),
    default=2,
    required=False,
    help="Set the period after which the info will be refreshed"
)
@option(
    "-i",
    "--images",
    "images",
    type=Path(exists=True),
    default=None,
    required=True,
    help="Set the location to where the images config is stored"
)
@version_option(
    version=__versdata__, prog_name="SyncStar by Akashdeep Dhar"
)
def main(port: int = 8080, repair: bool = False, period: int = 2, images: str = None) -> None:
    keep_config(port, repair, period)
    isos_config(images)
    meet()
    work()
