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
database.py

Local interface to the database. Lot of query over here.
"""

import sqlite3


class DbUtils:

    def __init__(self, path):
        self.path = path
        self._database = sqlite3.connect(path)
        self._cursor = self._database.cursor()

    def __repr__(self):
        return 'sqlite db %s' % (self.path)

    def query(self, query):
        self._cursor.execute(query)
        self.save()
        return self._cursor.fetchall()

    def save(self):
        self._database.commit()

    def add_session(self, session):
        query = """INSERT INTO main.sessions
            (%s) VALUES
            (\'%s\', \'%s\');""" % (
            ','.join(["username", "algorithm"]), session.username, session.algorithm)

        self.query(query)

    def select_all(self, table):
        return self.query("SELECT * FROM %s" % (table))

    def add_account(self, account, algorithm, session):
        query = """INSERT INTO main.accounts
        (%s) VALUES
        (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\');""" % (
            ','.join(["name", "password",
                      "attributes", "algorithm", "id_session"]),
            account.name, account.password,
            account.attributes, algorithm, session.username
        )

        self.query(query)

    def select_accounts(self, session):
        query = "SELECT * FROM accounts WHERE id_session=\'%s\';" % (
            session.username
        )

        return self.query(query)

    def remove_account(self, account, session):
        query = """DELETE FROM accounts
            WHERE id_session = \'%s\' AND name = \'%s\';""" % (
            session.username, account
        )

        self.query(query)

    def select_sessions_name(self):
        return self.query("SELECT username FROM sessions;")

    def edit_account(self, session, account_name, column, value):
        query = """UPDATE accounts SET %s = \'%s\' WHERE name = \'%s\' AND id_session = \'%s\';""" % (
            column, value, account_name, session
        )
        self.query(query)
  
    def get_default_algorithm(self, session):
        query = "SELECT algorithm FROM session WHERE username = \'%s\';" % (
            session
        )
        return self.query(query)
    
    def get_default_email(self, session):
        query = "SELECT email FROM session WHERE username = \'%s\';" % (
            session
        )
        return self.query(query)
