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


from syncstar.config import standard


class CompletionConfirmation:
    """
    Helper class for confirming if a long running task has completed
    """
    def __init__(self):
        self.qant = [0 for _ in range(standard.poll)]

    def __bool__(self) -> bool:
        return self.qant[0] != 0 and len(set(self.qant)) == 1

    def push(self, item: int) -> None:
        self.qant.append(item)
        self.qant.remove(self.qant[0])
