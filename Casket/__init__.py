import os
import sys
import sqlite3
import pickle
from pathlib import Path
import json

from .CryptoUtils import CryptoUtils

from PyQt5.QtWidgets import QApplication, QSplashScreen
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer

class Casket:

    def USER_CONFIG():
        with open('/'.join([Casket.HOME_PATH, 'config.json']), 'r') as outfile:
            return json.load(outfile)

    HOME_PATH = str(Path.home()) + '/Casket'

    SUBDIRS = [
    'db',
    'private'
    ]

    DB_PATH = '%s/%s/Casket.db' % (HOME_PATH, SUBDIRS[0])

    SUBFOLDERS = [
    HOME_PATH + '/' + SUBDIRS[0] + '/',
    HOME_PATH + '/' + SUBDIRS[1] + '/',
    ]

    MASTER_HASH_PATH = SUBFOLDERS[1] + 'Casket'

    def MASTER_HASH():
        with open(Casket.MASTER_HASH_PATH, 'rb') as filehandler:
            return pickle.load(filehandler)

    FIRST_START_VERIFIER_PATH = SUBFOLDERS[1] + 'FIRSTSTART'

    def FIRST_START():
        return os.path.isfile(Casket.FIRST_START_VERIFIER_PATH)

    def firstSetup():

        os.mkdir(Casket.HOME_PATH)

        for i in Casket.SUBDIRS:
            os.mkdir(Casket.HOME_PATH + '/' + i)

        data = {
        "first_start": "none"
        }

        with open('/'.join([Casket.HOME_PATH, 'config.json']), 'w') as outfile:
            json.dump(data, outfile)

        with open(Casket.FIRST_START_VERIFIER_PATH, 'w') as filehandler:

            try:
                pickle.dump('', filehandler)

            except:
                pass

        conn = sqlite3.connect(Casket.DB_PATH)
        os.system('sqlite3 %s < Casket/data/sql/structure.sql' % (Casket.DB_PATH))


    def startGui():

        from Casket.interface import IMain, ILogin

        app = QApplication(sys.argv)

        splash = QSplashScreen(QPixmap('Casket/resources/banner.png'), Qt.WindowStaysOnTopHint)
        splash.show()

        QTimer.singleShot(2000, lambda: splash.close())

        if not Casket.FIRST_START():

            login = ILogin()
            login.exec_()

            if login.verified:

                ui = IMain()
                sys.exit(app.exec_())

        else:

            ui = IMain()
            sys.exit(app.exec_())


    def startCli():
        pass
