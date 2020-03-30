"""
session.py

Main entry of casket module, it permit to manage all the casket's function,
create new sessions and add new accounts.
"""

__authors__ = "Jasoc"
__version__ = "0.1.beta1"
__license__ = "GNU General Public License v3.0"

import json
import casket


class session:

    def __init__(self, method, username, password_master,
                 email="user@example.com", algorithm="sha256"):

        self.username = username
        self.email = email
        self.password_master = password_master
        self.algorithm = algorithm
        self.accounts = {}
        self._decrypt = lambda s, m = self.password_master: casket.crypto.decrypt_password(m, s)

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
                    raise Exception("Wrong password.")
            else:
                raise Exception()
        else:
            raise Exception("invalid parameter")

    def new_account(self, account):

        if self.account_exists(account.name):
            raise Exception("Account name \'%s\' already exist." % (
                account.name)
                )
        else:
            a = account
            a.password = casket.crypto.encrypt_password(
                self.password_master, a.password)
            a.email = casket.crypto.encrypt_password(
                self.password_master, a.email)
            a.attributes = casket.crypto.encrypt_password(
            self.password_master, json.dumps(a.attributes))
            a.id_session = self.username
            self.db.add_account(a, self)
            self.sync_db()

    def remove_account(self, account_name):
        if self.account_exists(account_name):
            self.db.remove_account(account_name, self)
            self.sync_db()
        else:
            raise Exception("Account \'%s\' doesen't exists." % (account_name))

    def edit_account(self, account_name, column, new_value):
        if column in ['name', 'password', 'email']:
            if self.account_exists(account_name):
                if column != 'name':
                    new_value = casket.crypto.encrypt_password(
                        self.password_master, new_value)
                self.db.edit_account(self.username, account_name, column, new_value)
                self.sync_db()
            else:
                raise Exception("Account doesen't exist.")
        else:
            raise Exception("Invalid column.")

    def decrypt_accounts(self):
        self.sync_db()
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

    def account_exists(self, account_name):
        self.sync_db()
        return account_name in [_ for _ in self.accounts]