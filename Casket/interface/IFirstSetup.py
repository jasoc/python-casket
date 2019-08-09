import os
import pickle

from PyQt5.QtWidgets import QDialog, QLineEdit
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi

import Casket, CryptoUtils
from Casket.database import DbUtils
from Casket.interface import IFirstSetup

class IFirstSetup(QDialog):

    def __init__(self):

        super().__init__()
        loadUi('Casket/ui/first_setup.ui', self)

        self.initialize_component()

    def initialize_component(self):
        self.BTN_confirm.clicked.connect(self.BTN_confirm_FUNCT)
        self.TXT_key.setEchoMode(QLineEdit.Password)

    def BTN_confirm_FUNCT(self):

        master_hash = CryptoUtils.hash(self.TXT_key.text())

        with open(Casket.MASTER_HASH_PATH, 'wb') as filehandler:
            pickle.dump(master_hash, filehandler)

        os.system('rm ' + Casket.FIRST_START_VERIFIER_PATH)

        self.close()
