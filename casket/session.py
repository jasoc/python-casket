"""
session.py

Main entry of casket module, it permit to manage all the casket's function,
create new sessions and add new accounts.
"""

__authors__ = "Jasoc"
__version__ = "0.1.beta1"
__license__ = "GNU General Public License v3.0"

import casket

class session:

    def __init__(
        self,
        method,
        username,
        password_master,
        email = "user@example.com",
        algorithm = "sha256"
        ):

        self.username = username
        self.email = email
        self.password_master = password_master
        self.algorithm = algorithm
        self.accounts = {}

        if not casket.home.home_folder_exist():
            casket.home.make_folders()

        if method == "new":
            if not casket.home.check_user_exist(username):
                casket.home.make_user_folder(self)
                self.db = casket.database()
                self.db.add_session(self)
            else:
                raise casket.unable_to_open_session_exception("*** Session username already exist. ***")

        elif method == "load":
            if casket.home.check_user_exist(username):
                if self.check_password_master(self.password_master):
                    self.db = casket.database()
                    self.accounts = self.db.load_accounts(self)
                else:
                    raise Exception("password sbaglioata")
            else:
                raise Exception()
        else:
            raise Exception("invalid parameter")

    def new_account(self, account):
        if not account.name in [ _ for _ in self.accounts ]:
            account.id_session = self.username
            self.db.add_account(account, self)
            self.accounts = self.db.load_accounts(self)
        else:
            raise Exception("Account name \'%s\' already exist." % (account.name))

    def remove_account(self, account):
        if account in [ _ for _ in self.accounts ]:
            self.db.remove_account(account, self)
            self.accounts = self.db.load_accounts(self)
        else:
            raise Exception("Account \'%s\' doesen't exists." % (account))

    def decrypt_accounts(self):
        dict = {}
        self.accounts = self.db.load_accounts(self)
        for _ in self.accounts:
            temp = {}
            for __ in self.accounts[_].__dict__:
                try:
                    temp[__] = casket.crypto.decrypt_password(
                        self.password_master, self.accounts[_].__dict__[__])
                except Exception as e:
                    temp[__] = self.accounts[_].__dict__[__]
            dict[self.accounts[_].name] = temp
        return dict

    def check_password_master(self, password):
        return casket.crypto.check_hash(password, casket.home.master_hash(self.username))
