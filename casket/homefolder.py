"""
homefolder.py

Static class for manage the casket's folder in home dir.
"""

__authors__ = "Jasoc"
__version__ = "0.1.beta1"
__license__ = "GNU General Public License v3.0"

import os
import sys
import sqlite3
import datetime
import pickle
import json
from pathlib import Path

import casket


class homefolder:

    def __init__(self, folder_name='casket'):
        self.HOME_PATH = '%s/%s' % (str(Path.home()), folder_name)
        self.SUBDIRS = [
            'db',
            'private',
            'sessions'
        ]
        self.DB_PATH = '%s/%s/casket.db' % (self.HOME_PATH, self.SUBDIRS[0])
        self.SUBFOLDERS = ["%s/%s/" % (str(Path.home()) + '/casket', _)
                           for _ in self.SUBDIRS]

    def master_hash_path(self, username):
        return self.SUBFOLDERS[1] + username

    def user_config_path(self, username):
        return '/'.join([self.SUBFOLDERS[2], username, 'config.json'])

    def user_config(self, username):
        try:
            with open(self.user_config_path(username), 'r') as outfile:
                return json.load(outfile)
        except Exception as e:
            raise e

    def master_hash(self, username):
        try:
            with open(self.master_hash_path(username), 'rb') as filehandler:
                return pickle.load(filehandler)
        except Exception as e:
            raise e

    def make_folders(self):
        if not os.path.isdir(self.HOME_PATH):
            casket.log("Performing first setup.")
            os.mkdir(self.HOME_PATH)

            for _ in self.SUBFOLDERS:
                os.mkdir(_)

            conn = sqlite3.connect(self.DB_PATH)
            os.system('sqlite3 %s < casket/data/sql/structure.sql' %
                      (self.DB_PATH))
        else:
            raise Exception()

    def check_user_exist(self, user):
        return os.path.isdir("%s/%s" % (self.SUBFOLDERS[2], user))

    def homefolder_exist(self):
        return os.path.isdir(self.HOME_PATH)

    def make_user_folder(self, session):
        folder = self.SUBFOLDERS[2] + "/" + session.username

        if os.path.isdir(self.HOME_PATH):
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
                        session.password_master), filehandler)
            else:
                raise Exception()
        else:
            raise Exception()
