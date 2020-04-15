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
homefolder.py

Static class for manage the casket's folder in home dir.
"""

# TODO: fix home folder creation subroutine that create useless files and value.


import os
import sqlite3
import pickle
import json
from pathlib import Path

import casket


class HomeFolder:

    folder_name = "casket"
    home_path = '%s/%s' % (str(Path.home()), folder_name)
    subdirs = [
        'hashes',
    ]
    db_path = '%s/casket.db' % (home_path)
    subfolders = ["%s/%s/" % (str(Path.home()) + '/casket', _)
                  for _ in subdirs]

    @staticmethod
    def master_hash_path(username):
        return HomeFolder.subfolders[0] + username

    @staticmethod
    def master_hash(username):
        try:
            with open(HomeFolder.master_hash_path(username), 'rb') as filehandler:
                return pickle.load(filehandler)
        except Exception as exception:
            raise exception

    @staticmethod
    def make_folders():
        if not os.path.isdir(HomeFolder.home_path):
            os.mkdir(HomeFolder.home_path)

            for _ in HomeFolder.subfolders:
                os.mkdir(_)

            conn = sqlite3.connect(HomeFolder.db_path)
            os.system('sqlite3 %s < casket/data/sql/structure.sql' %
                      (HomeFolder.db_path))
        else:
            raise Exception()

    @staticmethod
    def check_user_exist(user):
        return os.path.isfile("%s/%s" % (HomeFolder.subfolders[0], user))

    @staticmethod
    def homefolder_exist():
        return os.path.isdir(HomeFolder.home_path)

    @staticmethod
    def make_user_folder(session, password_master):
        if not HomeFolder.check_user_exist(session.username):

            with open(HomeFolder.master_hash_path(session.username), 'wb') as filehandler:
                pickle.dump(casket.crypto.hash(
                    password_master), filehandler)
        else:
            raise Exception()