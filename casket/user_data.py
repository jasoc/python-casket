#!/usr/bin/env python3
""" user_data.py
    Main script of Casket for parse argument and start the program.
"""
__authors__ = "Jasoc"
__version__ = "0.1b1"
__license__ = "GNU General Public License v3.0"

import os
import sys
import sqlite3
import pickle
from pathlib import Path
import json

import casket

class user_data:

    HOME_PATH = str(Path.home()) + '/.casket'
    SUBDIRS = [
        'db',
        'private'
    ]
    DB_PATH = '%s/%s/casket.db' % (HOME_PATH, SUBDIRS[0])
    SUBFOLDERS = [
        HOME_PATH + '/' + SUBDIRS[0] + '/',
        HOME_PATH + '/' + SUBDIRS[1] + '/',
    ]
    MASTER_HASH_PATH = SUBFOLDERS[1] + 'casket'
    FIRST_START_VERIFIER_PATH = SUBFOLDERS[1] + 'FIRSTSTART'

    @staticmethod
    def user_config():
        with open('/'.join([Casket.HOME_PATH, 'config.json']), 'r') as outfile:
            return json.load(outfile)

    @staticmethod
    def master_hash():
        with open(user_data.MASTER_HASH_PATH, 'rb') as filehandler:
            return pickle.load(filehandler)

    @staticmethod
    def first_start():
        return os.path.isfile(user_data.FIRST_START_VERIFIER_PATH)

    @staticmethod
    def first_setup():
        casket.log("Performing first setup.")
        os.mkdir(user_data.HOME_PATH)
        for i in user_data.SUBDIRS:
            os.mkdir(user_data.HOME_PATH + '/' + i)
        data = {
            "first_start": "none"
        }
        with open('/'.join([user_data.HOME_PATH, 'config.json']), 'w') as outfile:
            json.dump(data, outfile)
        with open(user_data.FIRST_START_VERIFIER_PATH, 'w') as filehandler:
            try:
                pickle.dump('', filehandler)
            except:
                pass
        conn = sqlite3.connect(user_data.DB_PATH)
        os.system('sqlite3 %s < casket/data/sql/structure.sql' % (user_data.DB_PATH))
