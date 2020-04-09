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
import datetime
import pickle
import json
from pathlib import Path

import casket


class HomeFolder:

    def __init__(self, folder_name='casket'):
        self.home_path = '%s/%s' % (str(Path.home()), folder_name)
        self.subdirs = [
            'db',
            'private',
            'sessions'
        ]
        self.db_path = '%s/%s/casket.db' % (self.home_path, self.subdirs[0])
        self.subfolders = ["%s/%s/" % (str(Path.home()) + '/casket', _)
                           for _ in self.subdirs]

    def master_hash_path(self, username):
        return self.subfolders[1] + username

    def user_config_path(self, username):
        return '/'.join([self.subfolders[2], username, 'config.json'])

    def user_config(self, username):
        try:
            with open(self.user_config_path(username), 'r') as outfile:
                return json.load(outfile)
        except Exception as exception:
            raise exception

    def master_hash(self, username):
        try:
            with open(self.master_hash_path(username), 'rb') as filehandler:
                return pickle.load(filehandler)
        except Exception as exception:
            raise exception

    def make_folders(self):
        if not os.path.isdir(self.home_path):
            os.mkdir(self.home_path)

            for _ in self.subfolders:
                os.mkdir(_)

            conn = sqlite3.connect(self.db_path)
            os.system('sqlite3 %s < casket/data/sql/structure.sql' %
                      (self.db_path))
        else:
            raise Exception()

    def check_user_exist(self, user):
        return os.path.isdir("%s/%s" % (self.subfolders[2], user))

    def homefolder_exist(self):
        return os.path.isdir(self.home_path)

    def make_user_folder(self, session, password_master):
        folder = self.subfolders[2] + "/" + session.username

        if os.path.isdir(self.home_path):
            if not os.path.isdir(folder):
                os.mkdir(folder)

                data = {
                    "first_start": "none",
                    "username": session.username,
                    "email": session.email,
                    "date_creation": str(datetime.datetime.now()),
                    "default_algorithm": session.algorithm
                }

                with open(self.user_config_path(session.username), 'w+') as filehandler:
                    json.dump(data, filehandler)

                with open(self.master_hash_path(session.username), 'wb') as filehandler:
                    pickle.dump(casket.crypto.hash(
                        password_master), filehandler)
            else:
                raise Exception()
        else:
            raise Exception()
