import os
import sys
import sqlite3
from pathlib import Path
import json

from .Security import Security

from PyQt5.QtWidgets import QApplication, QSplashScreen
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer

class CASKET:

    def USER_CONFIG():
        with open('/'.join([CASKET.HOME_PATH, 'config.json']), 'r') as outfile:
            return json.load(outfile)

    HOME_PATH = str(Path.home()) + '/casket'

    SUBDIRS = [
    'db',
    'private'
    ]

    DB_PATH = '%s/%s/casket.db' % (HOME_PATH, SUBDIRS[0])

    SUBFOLDERS = [
    HOME_PATH + '/' + SUBDIRS[0] + '/',
    HOME_PATH + '/' + SUBDIRS[1] + '/',
    ]

    MASTER_HASH_PATH = SUBFOLDERS[1] + 'CASKET'

    FIRST_START_VERIFIER_PATH = SUBFOLDERS[1] + 'FIRSTSTART'

    FIRST_START():
        return os.path.isfile(FIRST_START_VERIFIER_PATH)

def firstSetup():

    os.mkdir(CASKET.HOME_PATH)

    for i in CASKET.SUBDIRS:
        os.mkdir(CASKET.HOME_PATH + '/' + i)

    data = {
    "first_start": "none"
    }

    with open('/'.join([CASKET.HOME_PATH, 'config.json']), 'w') as outfile:
        json.dump(data, outfile)

    with open(CASKET.FIRST_START_VERIFIER_PATH, 'w') as filehandler
        pickle.dump('', filehandler)

    conn = sqlite3.connect(CASKET.DB_PATH)
    os.system('sqlite3 %s < casket/data/sql/structure.sql' % (CASKET.DB_PATH))


def startGui():

    from casket.interface import IMain

    app = QApplication(sys.argv)

    splash = QSplashScreen(QPixmap('casket/resources/banner.png'), Qt.WindowStaysOnTopHint)
    splash.show()

    QTimer.singleShot(2000, lambda: splash.close())

    if not CASKET.FIRST_START():
        pass
        
    ui = IMain()

    sys.exit(app.exec_())


def startCli():
    pass
