"""
dbutils.py

Local interface to the database. Lot of query over here.
"""

__authors__ = "Jasoc"
__version__ = "0.1.beta1"
__license__ = "GNU General Public License v3.0"


import casket
import sqlite3


class dbutils:

    def __init__(self, path=casket.home.DB_PATH):
        self._database = sqlite3.connect(path)
        self._cursor = self._database.cursor()

    def __repr__(self):
        return 'sqlite db %s' % (casket.home.DB_PATH)

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

    def add_account(self, account, session):
        q = """INSERT INTO main.accounts
        (%s) VALUES
        (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\');""" % (
            ','.join(["name", "password", "email", "other_json", "id_session"]),
            account.name, account.password, account.email,
            account.attributes, session.username
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
        casket.log(q)
        self.query(q)