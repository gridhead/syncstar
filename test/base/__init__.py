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


class MockDeviceItem:
    def __init__(self, iden: str):
        self.ID_BUS = "usb"
        self.device_node = "/dev/null"
        self.device_number = "12121999"
        self.iden = iden
        self.size = 0
        self.properties = {
            "ID_SERIAL_SHORT": iden,
            "ID_VENDOR": iden,
            "ID_MODEL": iden,
        }

    def get(self, item: str):
        return self.ID_BUS


class MockDeviceList:
    def __init__(self, devs: list):
        self.devs = devs
        self.indx = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.indx < len(self.devs):
            item = self.devs[self.indx]
            self.indx += 1
            return item
        raise StopIteration
