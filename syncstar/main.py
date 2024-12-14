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
from syncstar.dyno import work


def meet() -> None:
    """
    Logs configuration details for the SyncStar service

    :return: None
    """
    view.success(f"Starting SyncStar v{__versdata__}...")


def meet_apim() -> None:
    """
    Logs configuration details for the apim service

    :return: None
    """
    view.warning(f"Authentication username. '{standard.username}'")
    view.warning(f"Authentication password. '{standard.password}'")
    view.warning(f"Debug mode is {'enabled' if standard.repair else 'disabled'}")


def meet_cell() -> None:
    """
    Logs configuration details for the cell service

    :return: None
    """
    view.warning(f"Images config - '{standard.images}'")
    view.warning(f"Broker source - '{standard.broker_link}'")
    view.warning(f"Result source - '{standard.result_link}'")


@group(
    name="syncstar",
    context_settings={"show_default": True},
    help="Starts the SyncStar service with the specified configuration",
)
@option(
    "-i",
    "--images",
    "images",
    type=Path(exists=True),
    default=None,
    required=True,
    help="Set the location to where the images config is stored."
)
@option(
    "-s",
    "--source",
    "source",
    type=Path(),
    default=standard.source,
    required=None,
    help="Set the location where tasks will be exchanged."
)
@option(
    "-r",
    "--repair",
    "repair",
    type=bool,
    default=standard.repair,
    required=False,
    help="Show the nerdy statistics to help repair the codebase."
)
@version_option(
    version=__versdata__, prog_name="SyncStar by Akashdeep Dhar"
)
def main(images: str = None, source: str = standard.source, repair: bool = False) -> None:
    """
    Starts the SyncStar service with the specified configuration

    The service command configures the frontend service by specifying the images configuration
    file, the source location for task exchange and whether to display the debugging statistics of
    the functional codebase.

    :param images: Path to the directory where the images configuration is stored
    :param source: Path to the location where tasks will be shared (defaults to `standard.source`)
    :param repair: Whether to display debugging statistics and active reloading during execution
    :return: None
    """
    config.main_config(images, source, repair)
    meet()


@main.command(
    name="apim",
    help="Start the frontend service",
    context_settings={"show_default": True},
)
@option(
    "-f",
    "--feed",
    "feed",
    type=str,
    default=[],
    required=False,
    multiple=True,
    help="Add the feed to read relevant recent information from."
)
@option(
    "-p",
    "--port",
    "port",
    type=IntRange(min=64, max=65535),
    default=8080,
    required=False,
    help="Set the port value for the service frontend endpoints."
)
@option(
    "-u",
    "--username",
    "username",
    type=str,
    default=standard.username,
    required=False,
    help="Set the username for service authentication."
)
@option(
    "-w",
    "--password",
    "password",
    type=str,
    default=standard.username,
    required=False,
    help="Set the password for service authentication."
)
def apim(
    feed: int = standard.fdlist,
    port: int = standard.port,
    username: str = standard.username,
    password: str = standard.password
) -> None:
    """
    Starts the frontend service with the specified configuration

    The `apim` command configures the frontend service by specifying the port number for service
    endpoints and credentials (username and password). Once configured, it initializes and starts
    the frontend service.

    :param port: Port for the service frontend endpoints (default: 8080) (range: 64 to 65535)
    :param username: Username for service authentication (defaults to `standard.username`)
    :param password: Password for service authentication (defaults to `standard.password`)
    :return: None
    """
    config.apim_config(feed, port, username, password)
    meet_apim()
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
    help="Set the number of concurrent worker tasks allowed."
)
@option(
    "-c",
    "--poll",
    "poll",
    type=IntRange(min=4, max=12),
    default=8,
    required=False,
    help="Set the number of completion checks for termination."
)
def cell(proc: int = standard.proc, poll: int = standard.poll) -> None:
    """
    Starts the worker service with the specified configuration

    The `cell` command configures the worker service by setting the number of concurrent worker
    tasks and completion checks for termination. Once configured, it initializes and starts the
    worker management system.

    :param proc: Number of concurrent worker tasks allowed (default: 8) (range: 4 to 20)
    :param poll: Number of completion checks for termination (default: 8) (range: 4 to 12)
    :return: None
    """
    config.cell_config(proc, poll)
    meet_cell()
    workobjc = task.taskmgmt.Worker(concurrency=standard.proc)
    workobjc.start()
