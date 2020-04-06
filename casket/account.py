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


class account:

    name = ''
    email = ''
    id_session = ''
    password = ''
    attributes = {}

    def __init__(self, name='default account', email="user@example.com",
                 password="casket", attributes={}):
        self.name = name
        self.email = email
        self.attributes = attributes
        self.password = password

    def __repr__(self):
        return "%s account(%s)" % (self.name, self.email)

    def set_password_safe(self, password):
        """if not casket.password_validator.check_exist(password):
            if casket.password_validator.check_string(password):
                self.password = password
            else:
                raise not_valid_password_error
        else:
            if casket.settings.equal_password_allowed:
                self.password = password
            else:
                raise not_valid_password_error"""
        self.password = password

    def set_password_any(self, password):
        self.password = password
