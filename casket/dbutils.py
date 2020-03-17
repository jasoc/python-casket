"""
dbutils.py

Local interface to the database. Lot of query over here.
"""

__authors__ = "Jasoc"
__version__ = "0.1.beta1"
__license__ = "GNU General Public License v3.0"


import json
import casket

class dbutils:

    def __init__(self):
        self._db = casket.sqlutils(casket.home.DB_PATH)

    def __repr__(self):
        return 'sqlite db %s' % (casket.home.DB_PATH)

    def add_session(self, session):
        self._db.query("INSERT INTO main.sessions (%s) VALUES (\'%s\', \'%s\');" % (','.join(["username", "email"]), session.username, session.email))

    def select_all(self, table):
        return self._db.query("SELECT * FROM %s" % (table))

    def add_account(self, account, session):
        a = account
        a.password = casket.crypto.encrypt_password(session.password_master, a.password)
        a.email = casket.crypto.encrypt_password(session.password_master, a.email)
        a.attributes = casket.crypto.encrypt_password(session.password_master, json.dumps(a.attributes))

        q = "INSERT INTO main.accounts (%s) VALUES (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\');" % (','.join(["name", "pswd", "email", "other_json", "id_session"]), a.name, a.password, a.email, a.attributes, session.username)
        self._db.query(q)


    def load_accounts(self, session):
        q = "SELECT * FROM accounts WHERE id_session=\'%s\';" % (session.username)
        res = self._db.query(q)
        ret = {}
        for _ in res:
            temp = casket.account()
            temp.name = _[1]
            temp.password = _[2]
            temp.email = _[3]
            temp.attributes = _[4]
            temp.id_session = _[5]
            ret[temp.name] = temp
        return ret

    def remove_account(self, account, session):
        q = "DELETE FROM accounts WHERE id_session = \'%s\' AND name = \'%s\' ;" % (session.username, account)
        self._db.query(q)


    def select_sessions_name(self):
        return self._db.query("SELECT username FROM sessions;")
