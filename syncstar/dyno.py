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


from flask import Flask

from syncstar import __projname__
from syncstar.config import standard
from syncstar.root import root


def main():
    serv = Flask(
        import_name=__projname__,
        template_folder="frontend",
        static_folder="frontend/assets"
    )
    serv.register_blueprint(root)
    serv.secret_key = standard.secret
    return serv


def work() -> None:
    """
    Starts the application service on all interfaces with the defined config data

    :return:
    """
    serv = main()
    serv.run(
        host="0.0.0.0",  # noqa : S104
        port=standard.port,
        debug=standard.repair
    )
