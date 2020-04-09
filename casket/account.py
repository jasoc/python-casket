# -*- coding: utf-8 -*-
# Casket python module
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, see <http://www.gnu.org/licenses/>.

"""
account.py

Mockup class that represent the casket's accounts.
"""


class Account:

    name = ''
    email = ''
    id_session = ''
    password = ''
    attributes = {}

    def __init__(self, name='default account', email="user@example.com",
                 password="casket"):
        self.name = name
        self.email = email
        self.attributes = {}
        self.password = password

    def __repr__(self):
        return "%s account(%s)" % (self.name, self.email)
