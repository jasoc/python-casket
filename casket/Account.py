from casket import CryptoUtils


class Account:

    def __init__(self, name, pswd = None):

        self._name = name
        self._pswd = pswd

        self.pswd_present = pswd is not None

        self._db = Database()


    def __repr__(self):
        return self._name + ' account'


    def name(self):
        return self._name


    def changeName(self, new_name):
        self._name = new_name


    def changePassword(self, new_pswd):
        self._pswd = new_pswd


    def store(self):

        enc_pswd = Security.encryptPassword(self._pswd)
        self._db.addRow(self._name, enc_pswd)
