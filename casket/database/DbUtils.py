import sqlite3
from .SqlUtils import SqlUtils
from casket import CASKET

class DbUtils:

    def __init__(self):

        self._db = SqlUtils(CASKET.DB_PATH)

    def __repr__(self):
        return 'sqlite db'

    def rowsCount(self, table):
        return len(self._db.query('SELECT * FROM ' + table))

    def columnsCount(self, table):
        return len(self.getColumnsNames(table))

    def addRow(self, values, table):

        try:
            self._db.query('INSERT INTO %s (%s) VALUES (%s)' % (table, ', '.join(self.getColumnsNames(table)), ', '.join(values)))

        except Exception as e:
            raise Exception('Invalid parameters /n' + e)

    def getColumnsNames(self, table):
        """
        return self.query("SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_SCHEMA`='" +
        table +
        "' +
        """

        return ['name','pswd']

    def getPswd(name):
        return self._db.query("SELECT pswd FROM accounts WHERE name='%s'" % (name))
