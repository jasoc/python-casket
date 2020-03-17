"""
sqlutils.py

Support file for querying local sqlite3 databases.
"""

__authors__ = "Jasoc"
__version__ = "0.1.beta1"
__license__ = "GNU General Public License v3.0"


import sqlite3

class sqlutils:

    def __init__(self, path):
        self._database = sqlite3.connect(path)
        self._cursor = self._database.cursor()

    def __repr__(self):
        return 'sqlite db'

    def save(self):
        self._database.commit()

    def query(self, query, void=False):
        ready = False
        self._cursor.execute(query)
        self.save()
        return self._cursor.fetchall()
