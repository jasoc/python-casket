import os
import pickle

from PyQt5.QtWidgets import QDialog, QLineEdit
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi

import Casket, CryptoUtils
from Casket.database import DbUtils
from Casket.interface import IFirstSetup

class ILogin(QDialog):

    def __init__(self):

        super().__init__()
        loadUi('Casket/resources/ui/login.ui', self)

        self.verified = False
        self.initialize_component()

    def initialize_component(self):
        self.BTN_confirm.clicked.connect(self.BTN_confirm_FUNCT)
        self.TXT_pswd.setEchoMode(QLineEdit.Password)

    def BTN_confirm_FUNCT(self):

        if CryptoUtils.checkHash(self.TXT_pswd.text(), Casket.MASTER_HASH()):
            self.verified = True
            self.close()

        else:
            self.BTN_confirm.setText('Retry')
