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

from logzero import logger

from .cryptography import cryptoutils as crypto
from .homefolder import homefolder as home
from .database import dbutils as database
from .session import session
from .exceptions import *
from .account import account


def log(arg):
    logger.info(str(arg))


def load_session(username, password):
    return session(method="load", username=username, password_master=password)


def new_session(username, password, email, default_algorithm="sha256"):
    return session(method="new", username=username, password_master=password, email=email, algorithm=default_algorithm)


def sessions_list():
    h = home()
    res = database(h.DB_PATH).select_sessions_name()
    return [_[0] for _ in res]
