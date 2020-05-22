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
self.py

Static class for manage the casket's folder in home dir.
"""

import sys
import os
import sqlite3
import pickle
import json
from pathlib import Path

import casket


class WorkSpace:

    def __init__(self, path="default"):

        if path=="default":
            if sys.platform == "linux" or sys.platform == "linux2" or sys.platform == "darwin":
                self.home_path = '%s/casket' % (str(Path.home()))
            else:
                self.home_path = 'C://casket'
        else:
            if path.endswith('/') or path.endswith('\\'):
                self.home_path = casket_path[:-1]
            else:
                self.home_path = casket_path


        self.subdirs = [
            'hashes',
        ]

        self.db_path = '%s/casket.db' % (self.home_path)
        self.subfolders = ["%s/%s/" % (self.home_path, _)
                      for _ in self.subdirs]

        if not self.self_exist():
            self.make_folder()

    def master_hash_path(self, username):
        return self.subfolders[0] + username

    def db_object(self):
        with open(self.db_path) as db:
            return db

    def master_hash(self, username):
        try:
            with open(self.master_hash_path(username), 'rb') as filehandler:
                return pickle.load(filehandler)
        except Exception as exception:
            raise exception

    def make_folder(self):
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
        return os.path.isfile("%s/%s" % (self.subfolders[0], user))

    def self_exist(self):
        return os.path.isdir(self.home_path)

    def make_user_folder(self, session, password_master):
        if not self.check_user_exist(session.username):

            with open(self.master_hash_path(session.username), 'wb') as filehandler:
                pickle.dump(casket.crypto.hash(
                    password_master), filehandler)
        else:
            raise Exception()

    def load_session(self, username, password):
        return casket.Session(self, method="load", username=username, password_master=password)

    def new_session(self, username, password, default_algorithm="sha256"):
        return casket.Session(self, method="new", username=username, password_master=password, algorithm=default_algorithm)

    def list_sessions(self):
        res = casket.database(self.db_path).select_sessions_name()
        return [_[0] for _ in res]
