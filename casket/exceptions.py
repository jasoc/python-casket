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


# TODO: fix naming style of exception classes and change it in all other files.


class unable_to_open_session_exception(Exception):
    """Exception raised when it is impossible to open a session."""
    pass


class wrong_password(Exception):
    """Exception raised for errors in the input of the password."""
    pass


class user_doesnt_exist(Exception):
    """Exception raised when the user doesn't exist."""
    pass


class invalid_parameter(Exception):
    """Exception raised when entered an invalid parameter."""
    pass


class account_name_already_exist(Exception):
    """Exception raised when the account name already exist."""
    pass


class account_doesnt_exist(Exception):
    """Exception raised when the account doesn't exist."""
    pass


class invalid_algorithm(Exception):
    """Exception raised when user instert manually an inexistent algorithm."""
    pass
