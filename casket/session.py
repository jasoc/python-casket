# -*- coding: utf-8 -*-
# Casket
# Copyright (c) 2009, Paride Giunta <paridegiunta@gmail.com>
# Copyright (c) 2009, Riccardo Nuncibello <riccardo.n1402@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, see <http://www.gnu.org/licenses/>.

"""
session.py

Main entry of casket module, it permit to manage all the casket's function,
create new sessions and add new accounts.
"""

import json
import casket


class session:
    """Main class of Casket.
    Args:
        method:          The method the user want to access,
                         'new' for new user, 'load' for load an already created session.
        username:        The username of user's choise.
        password_master: Password master of Casket.
        email:           Default email user want to use for acount.
        algorithm:       Default algorithm the user want to set.
    """

    def __init__(self, method, username, password_master,
                 email="user@example.com", algorithm="sha256"):

        self.username = username
        self.email = email
        self.password_master = password_master
        self.algorithm = algorithm
        self.accounts = {}
        self._decrypt = lambda s, a, m = self.password_master: casket.crypto.decrypt_password(
            m, s, algorithm=a)

        self.home = casket.home()
        if not self.home.homefolder_exist():
            self.home.make_folders()

        if method == "new":
            if not self.home.check_user_exist(username):
                self.home.make_user_folder(self)
                self.db = casket.database(self.home.DB_PATH)
                self.db.add_session(self)
            else:
                raise casket.unable_to_open_session_exception(
                    "*** Session username already exist. ***"
                )

        elif method == "load":
            if self.home.check_user_exist(username):
                if self.check_password_master(self.password_master):
                    self.db = casket.database(self.home.DB_PATH)
                    self.sync_db()
                else:
                    raise casket.wrong_password("Wrong password.")
            else:
                raise casket.user_doesnt_exist("User doesn't exist.")
        else:
            raise casket.invalid_parameter("Invalid method \'%s\'." % (method))

    def new_account(self, account, algorithm):
        """Add a new account object to the database."""

        if self.account_exists(account.name):
            raise casket.account_name_already_exist("Account name \'%s\' already exist." % (
                account.name))

        else:
            a = account
            a.password = casket.crypto.encrypt_password(
                self.password_master, a.password, algorithm=algorithm)

            a.email = casket.crypto.encrypt_password(
                self.password_master, a.email, algorithm=algorithm)

            a.attributes = casket.crypto.encrypt_password(
                self.password_master, json.dumps(a.attributes), algorithm=algorithm)

            a.id_session = self.username
            self.db.add_account(a, algorithm, self)
            self.sync_db()

    def remove_account(self, account_name):
        """Remove given account from database."""
        if self.account_exists(account_name):
            self.db.remove_account(account_name, self)
            self.sync_db()
        else:
            raise casket.account_doesnt_exist("Account \'%s\' doesen't exists." % (account_name))

    def edit_account(self, account_name, column, new_value):
        """Creates a model for a combobox showing factories.
        Args:
            account_name (srt): Name of the account user want to edit.
            column (str):       Attribute of account to edit.
            new_value (str):    New value to set.
        """
        if column in ['name', 'password', 'email']:
            if self.account_exists(account_name):
                if column != 'name':
                    new_value = casket.crypto.encrypt_password(
                        self.password_master, new_value, algorithm=self.accounts[account_name].algorithm)
                self.db.edit_account(
                    self.username, account_name, column, new_value)
                self.sync_db()
            else:
                raise Exception("Account doesen't exist.")
        else:
            raise Exception("Invalid column.")

    def decrypt_accounts(self):
        """Return a dictionary with all the accounts with
        a lambda for decrypt the credentials.
        """
        self.sync_db()

        def dec_exp(str, alg):
            try:
                return self._decrypt(str, alg)
            except Exception:
                return str

        return {_: {__: dec_exp(self.accounts[_].__dict__[__], self.accounts[_].__dict__["algorithm"])
                    for __ in self.accounts[_].__dict__}
                for _ in self.accounts}

    def check_password_master(self, password):
        """Check if given password match the saved hash."""
        return casket.crypto.check_hash(
            password, self.home.master_hash(
                self.username))

    def sync_db(self):
        """Query the DB for syncronize the attribute with new values."""
        res = self.db.select_accounts(self)

        def build_acc(_):
            temp = casket.account(_[1], _[3], _[2], _[4])
            temp.id_session = _[6]
            temp.algorithm = _[5]
            return temp

        self.accounts = {_[1]: build_acc(_) for _ in res}

    def account_exists(self, account_name):
        """Check if geven account exists."""
        self.sync_db()
        return account_name in [_ for _ in self.accounts]
