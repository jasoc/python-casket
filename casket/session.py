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

    def __init__(self, method, username, password_master,
                 email="user@example.com", algorithm="sha256"):

        self.username = username
        self.email = email
        self.password_master = password_master
        self.algorithm = algorithm
        self.accounts = {}
        self._decrypt = lambda s, m = self.password_master:
            casket.crypto.decrypt_password(m, s)

        if not casket.home.homefolder_exist():
            casket.home.make_folders()

        if method == "new":
            if not casket.home.check_user_exist(username):
                casket.home.make_user_folder(self)
                self.db = casket.database()
                self.db.add_session(self)
            else:
                raise casket.unable_to_open_session_exception(
                    "*** Session username already exist. ***")

        elif method == "load":
            if casket.home.check_user_exist(username):
                if self.check_password_master(self.password_master):
                    self.db = casket.database()
                    self.sync_db()
                else:
                    raise casket.wrong_password("Wrong password.")
            else:
                raise casket.user_doesnt_exist("User doesn't exist.")
        else:
            raise casket.invalid_parameter("Invalid method \'%s\'." % (method))

    def new_account(self, account):
        if account.name in [_ for _ in self.accounts]:
            raise casket.account_name_already_exist("Account name \'%s\' already exist." % (
                account.name))
        else:
            account.id_session = self.username
            self.db.add_account(account, self)
            self.sync_db()

    def remove_account(self, account):
        if account in [_ for _ in self.accounts]:
            self.db.remove_account(account, self)
            self.accounts = self.db.load_accounts(self)
        else:
            raise casket.account_doesnt_exist("Account \'%s\' doesen't exists." % (account))

    def decrypt_accounts(self):
        def dec_exp(str):
            try:
                return self._decrypt(str)
            except Exception as e:
                return str
        return {_: {__: dec_exp(self.accounts[_].__dict__[__])
                for __ in self.accounts[_].__dict__}
                for _ in self.accounts}

    def check_password_master(self, password):
        return casket.crypto.check_hash(
            password, casket.home.master_hash(
                self.username))

    def sync_db(self):
        res = self.db.select_accounts(self)

        def build_acc(_):
            temp = casket.account(_[1], _[3], _[2], _[4])
            temp.id_session = _[5]
            return temp

        self.accounts = {_[1]: build_acc(_) for _ in res}
