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
        email = "user@example.com",
        password_master = "casket",
        algorithm = "sha256"
        ):

        self.username = username
        self.email = email
        self.password_master = password_master
        self.algorithm = algorithm
        self.accounts = []

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
                if casket.crypto.check_hash(self.password_master, casket.home.master_hash(self.username)):
                    self.db = casket.database()
                    self.accounts = self.db.load_accounts(self)
                else:
                    raise Exception("password sbaglioata")
            else:
                raise Exception()
        else:
            raise Exception("invalid parameter")

    def new_account(self, account):
        if not account.name in [ _.name for _ in self.accounts ]:
            self.db.add_account(account, self)
            self.accounts = self.db.load_accounts(self)
        else:
            raise Exception("Account name \'%s\' already exist." % (account.name))

    def remove_account(self, account):
        if account in [ _.name for _ in self.accounts ]:
            self.db.remove_account(account, self)
            self.accounts = self.db.load_accounts(self)
        else:
            raise Exception("Account \'%s\' doesen't exists." % (account))
