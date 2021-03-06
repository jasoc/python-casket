# -*- coding: utf-8 -*-
# Casket python module
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
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

# TODO: fix exceptions managing.

import csv
import json
import casket


class Session:
    """Main class of Casket.
    Args:
            method:          The method the user want to access,
                             'new' for new user, 'load' for load an already created session.
            username:        The username of user's choise.
            password_master: Password master of Casket.
            email:           Default email user want to use for acount.
            algorithm:       Default algorithm the user want to set.
    """

    def __init__(self, workspace, method, username,
                 password_master, algorithm="sha256"):

        self.username = username
        self.algorithm = algorithm
        self.workspace = workspace
        self.accounts = {}

        if method == "new":
            if not self.workspace.check_user_exist(username):
                self.workspace.make_user_folder(self, password_master)
                self.database = casket.database(self.workspace.db_path)
                self.database.add_session(self)
            else:
                raise casket.unable_to_open_session_exception(
                    "Session username already exist.")

        elif method == "load":
            if self.workspace.check_user_exist(username):
                if self.check_password_master(password_master):
                    self.database = casket.database(self.workspace.db_path)
                    self.sync_db()
                else:
                    raise casket.wrong_password("Wrong password.")
            else:
                raise casket.user_doesnt_exist("User doesn't exist.")
        else:
            raise casket.invalid_parameter("Invalid method \'%s\'." % (method))

    def new_account(self, account, password_master, algorithm="default"):
        """Add a new account object to the database."""
        if not self.check_password_master(password_master):
            raise Exception("Wrong password.")

        if algorithm == "default":
            algorithm = self.algorithm
        if not self.account_exists(account.name):
            temp_account = account

            temp_account.password = casket.crypto.encrypt_password(
                password_master, temp_account.password, algorithm=algorithm)

            temp_account.attributes = casket.crypto.encrypt_password(
                password_master, json.dumps(temp_account.attributes), algorithm=algorithm)

            temp_account.id_session = self.username
            self.database.add_account(temp_account, algorithm, self)
            self.sync_db()
        else:
            raise casket.account_name_already_exist("Account name \'%s\' already exist." % (
                account.name))

    def remove_account(self, account_name):
        """Remove given account from database."""
        if self.account_exists(account_name):
            self.database.remove_account(account_name, self)
            self.sync_db()
        else:
            raise casket.account_doesnt_exist(
                "Account \'%s\' doesen't exists." % (account_name))

    def edit_account(self, account_name, column, new_value, password_master):
        """Creates a model for a combobox showing factories.
        Args:
                account_name (str): Name of the account user want to edit.
                column (str):       Attribute of account to edit.
                new_value (str):    New value to set.
        """
        if not self.check_password_master(password_master):
            raise Exception("Wrong password.")

        if column in ['name', 'password', 'attributes']:
            if self.account_exists(account_name):
                if column != "name":
                    new_value = casket.crypto.encrypt_password(
                        password_master, new_value,
                        algorithm=self.accounts[account_name].algorithm)
                self.database.edit_account(
                    self.username, account_name, column, new_value)
                self.sync_db()
            else:
                raise Exception("Account doesen't exist.")
        else:
            raise Exception("Invalid column.")

    def get_decrypted_value(self, account, value, password_master):
        """Return passed value of passed account decrypted."""
        if not self.check_password_master(password_master):
            raise Exception("Wrong password.")

        self.sync_db()

        if value != "name":
            raw_value = self.accounts[account].__dict__[value]
            algorithm = self.accounts[account].__dict__['algorithm']
            return casket.crypto.decrypt_password(password_master, raw_value, algorithm)
        else:
            return account

    def get_decrypted_account_object(self, account_name, password_master):
        account = casket.Account()

        account.name = account_name
        account.password = casket.crypto.decrypt_password(password_master,
            self.accounts[account_name].__dict__['password'], self.accounts[account_name].__dict__['algorithm'])
        attributes = casket.crypto.decrypt_password(password_master,
            self.accounts[account_name].__dict__['attributes'], self.accounts[account_name].__dict__['algorithm'])
        account.attributes = json.loads(attributes)
        account.algorithm = self.accounts[account_name].__dict__['algorithm']

        return account

    def check_password_master(self, password):
        """Check if given password match the saved hash."""
        return casket.crypto.check_hash(
            password, self.workspace.master_hash(
                self.username))

    def sync_db(self):
        """Query the DB for syncronize the attribute with new values."""
        res = self.database.select_accounts(self)

        def build_acc(account):
            temp = casket.Account(account[1], account[2], account[3])
            temp.id_session = account[5]
            temp.algorithm = account[4]
            return temp

        self.accounts = {_[1]: build_acc(_) for _ in res}

    def account_exists(self, account_name):
        """Check if geven account exists."""
        self.sync_db()
        return account_name in self.accounts

    def default_algorithm(self):
        return self.database.get_default_algorithm(self.username)[0]

    def export(self, path, decrypted=True, filetype="csv", password_master="", delimiter=","):

        if decrypted:
            if password_master == "" and not self.check_password_master(password_master):
                raise Exception()
            with open('%s/casket.csv' % (path), mode='w') as casket_csv:
                writer = csv.writer(casket_csv, delimiter=delimiter, quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for account in self.accounts:
                    arr = []
                    for value in self.accounts[account].__dict__:
                        if value in ['name', 'password', 'attributes']:
                            new_value = casket.crypto.decrypt_password(password_master,
                                self.accounts[account].__dict__[value],
                                self.accounts[account].__dict__["algorithm"])
                        else:
                            new_value = self.accounts[account].__dict__[value]
                        arr.append(new_value)
                    writer.writerow(arr)
        else:
            with open('%s/casket.csv' % (path), mode='w') as casket_csv:
                writer = csv.writer(casket_csv, delimiter=delimiter, quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for account in self.accounts:
                    writer.writerow([self.accounts[account].__dict__[_] for _ in self.accounts[account].__dict__])