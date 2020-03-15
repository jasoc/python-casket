"""
home_folder.py

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

class home_folder:

    HOME_PATH = str(Path.home()) + '/casket'
    SUBDIRS = ['db', 'private', 'sessions']
    DB_PATH = '%s/%s/casket.db' % (HOME_PATH, SUBDIRS[0])
    SUBFOLDERS = [ "%s/%s/" %(str(Path.home()) + '/casket', _) for _ in SUBDIRS ]

    def master_hash_path(username):
        return home_folder.SUBFOLDERS[1] + username

    def user_config_path(username):
        return '/'.join([home_folder.SUBFOLDERS[2], username, 'config.json'])

    def user_config(username):
        try:
            with open(user_config_path(username), 'r') as outfile:
                return json.load(outfile)
        except Exception as e:
            raise e

    def master_hash(username):
        try:
            with open(home_folder.master_hash_path(username), 'rb') as filehandler:
                return pickle.load(filehandler)
        except Exception as e:
            raise e

    def make_folders():
        if not os.path.isdir(home_folder.HOME_PATH):
            casket.log("Performing first setup.")
            os.mkdir(home_folder.HOME_PATH)
            for i in home_folder.SUBFOLDERS:
                os.mkdir(i)
            conn = sqlite3.connect(home_folder.DB_PATH)
            os.system('sqlite3 %s < casket/data/sql/structure.sql' % (home_folder.DB_PATH))
        else:
            raise exception()

    def check_user_exist(user):
        return os.path.isdir("%s/%s" % (home_folder.SUBFOLDERS[2], user))

    def home_folder_exist():
        return os.path.isdir(home_folder.HOME_PATH)

    def make_user_folder(session):
        folder = home_folder.SUBFOLDERS[2] + "/" + session.username
        if os.path.isdir(home_folder.HOME_PATH):
            if not os.path.isdir(folder):
                os.mkdir(folder)
                data = {
                    "first_start": "none",
                    "username": session.username,
                    "email": session.email,
                    "date_creation": str(datetime.datetime.now()),
                    "default_algorithm": session.algorithm
                }
                with open(home_folder.user_config_path(session.username), 'w+') as filehandler:
                    json.dump(data, filehandler)
                with open(home_folder.master_hash_path(session.username), 'wb') as filehandler:
                    pickle.dump(casket.crypto.hash(session.password_master), filehandler)
            else:
                raise Exception()
        else:
            raise Exception()
