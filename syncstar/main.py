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


from click import IntRange, Path, group, option, version_option

from syncstar import __versdata__, config, task, view
from syncstar.config import standard
from syncstar.root import work


def meet() -> None:
    view.success(
        f"Starting SyncStar v{__versdata__}..."
    )


def meet_apim() -> None:
    view.warning(
        f"Use the secret code '{standard.code}' to authenticate with the service"
    )
    view.warning(
        f"Information on the frontend would be refreshed every after {standard.period} second(s)"
    )
    view.warning(
        f"Debug mode is {'enabled' if standard.repair else 'disabled'}"
    )


def meet_cell() -> None:
    view.warning(
        f"Images config - '{standard.images}'"
    )
    view.warning(
        f"Broker source - '{standard.broker_link}'"
    )
    view.warning(
        f"Result source - '{standard.result_link}'"
    )


@group(
    name="syncstar",
    context_settings={"show_default": True},
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
@option(
    "-s",
    "--source",
    "source",
    type=Path(),
    default=standard.source,
    required=None,
    help="Set the location where tasks will be exchanged"
)
@option(
    "-r",
    "--repair",
    "repair",
    type=bool,
    default=standard.repair,
    required=False,
    help="Show the nerdy statistics to help repair the codebase"
)
@version_option(
    version=__versdata__, prog_name="SyncStar by Akashdeep Dhar"
)
def main(images: str = None, source: str = standard.source, repair: bool = False) -> None:
    meet()
    config.main_config(images, source, repair)


@main.command(
    name="apim",
    help="Start the frontend service",
    context_settings={"show_default": True},
)
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
    "-t",
    "--period",
    "period",
    type=IntRange(min=2, max=30),
    default=2,
    required=False,
    help="Set the period after which the info will be refreshed"
)
def apim(port: int = standard.port, period: int = standard.period) -> None:
    meet_apim()
    config.apim_config(port, period)
    work()


@main.command(
    name="cell",
    help="Start the worker service",
    context_settings={"show_default": True},
)
@option(
    "-p",
    "--proc",
    "proc",
    type=IntRange(min=4, max=20),
    default=8,
    required=False,
    help="Set the number of concurrent worker tasks allowed"
)
@option(
    "-c",
    "--compct",
    "compct",
    type=IntRange(min=4, max=12),
    default=8,
    required=False,
    help="Set the number of completion checks for termination"
)
def cell(proc: int = standard.proc, compct: int = standard.compct) -> None:
    meet_cell()
    config.cell_config(proc, compct)
    workobjc = task.taskmgmt.Worker(concurrency=standard.proc)
    workobjc.start()
