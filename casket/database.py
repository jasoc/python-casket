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
dbutils.py

Local interface to the database. Lot of query over here.
"""

import casket
import sqlite3


class dbutils:

    def __init__(self, path):
        self.path = path
        self._database = sqlite3.connect(path)
        self._cursor = self._database.cursor()

    def __repr__(self):
        return 'sqlite db %s' % (self.path)

    def query(self, query, void=False):
        self._cursor.execute(query)
        self.save()
        return self._cursor.fetchall()

    def save(self):
        self._database.commit()

    def add_session(self, session):
        q = """INSERT INTO main.sessions
            (%s) VALUES
            (\'%s\', \'%s\');""" % (
            ','.join(["username", "email"]), session.username, session.email)

        self.query(q)

    def select_all(self, table):
        return self.query("SELECT * FROM %s" % (table))

    def add_account(self, account, algorithm, session):
        q = """INSERT INTO main.accounts
        (%s) VALUES
        (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\');""" % (
            ','.join(["name", "password", "email",
                      "other_json", "algorithm", "id_session"]),
            account.name, account.password, account.email,
            account.attributes, algorithm, session.username
        )

        self.query(q)

    def select_accounts(self, session):
        q = "SELECT * FROM accounts WHERE id_session=\'%s\';" % (
            session.username
        )

        return self.query(q)

    def remove_account(self, account, session):
        q = """DELETE FROM accounts
            WHERE id_session = \'%s\' AND name = \'%s\';""" % (
            session.username, account
        )

        self.query(q)

    def select_sessions_name(self):
        return self.query("SELECT username FROM sessions;")

    def edit_account(self, session, account_name, column, value):
        q = """UPDATE accounts SET %s = \'%s\' WHERE name = \'%s\' AND id_session = \'%s\';""" % (
            column, value, account_name, session
        )
        self.query(q)
