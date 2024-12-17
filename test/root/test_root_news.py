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


from json import loads

import pytest

from syncstar.config import standard


@pytest.mark.parametrize(
    "feed, name, desc, work",
    [
        pytest.param(
            "https://gridhead.net/feed",
            "Akashdeep Dhar",
            "A place for creative engineering that brings out the best in people",
            True,
            id="NEWS Endpoint - Akashdeep Dhar",
        ),
        pytest.param(
            "https://fedoramagazine.org/feed",
            "Fedora Magazine",
            "Guides, information, and news about the Fedora operating system for users, developers, system administrators, and community members.",
            True,
            id="NEWS Endpoint - Fedora Magazine",
        ),
        pytest.param(
            "https://communityblog.fedoraproject.org/feed",
            "Fedora Community Blog",
            "The Community Blog provides a single source for members of the community to share important news, updates, and information about Fedora with others in the Project community.",
            True,
            id="NEWS Endpoint - Fedora Commblog",
        ),
        pytest.param(
            "https://gridhead.net/fail",
            "UNOBTAINABLE",
            "UNOBTAINABLE",
            False,
            id="NEWS Endpoint - Unobtainable Resource",
        ),
    ]
)
def test_news(client, mocker, feed, name, desc, work):
    # Initialization
    mocker.patch("syncstar.config.standard.fdlist", [feed])

    mocker.patch("syncstar.config.standard.username", "username")
    mocker.patch("syncstar.config.standard.password", "password")
    head = {"username": standard.username, "password": standard.password}
    response = client.post("/sign", headers=head)
    assert response.status_code == 200

    # Confirmation
    response = client.get("/news")
    assert response.status_code == 200

    assert feed in loads(response.data.decode())["data"].keys()
    assert isinstance(loads(response.data.decode())["time"], str)
    assert name == loads(response.data.decode())["data"][feed]["head"]
    assert desc == loads(response.data.decode())["data"][feed]["desc"]

    if work:
        assert len(loads(response.data.decode())["data"][feed]["data"].keys()) > 0
    else:
        assert len(loads(response.data.decode())["data"][feed]["data"].keys()) == 0

    # Teardown
    response = client.post("/exit")
    assert response.status_code == 200
