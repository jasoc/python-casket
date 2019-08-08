import sqlite3

class Database:

    def __init__(self, path):

        self._database = sqlite3.connect(path)
        self._cursor = self._database.cursor()

    def __repr__(self):
        return 'sqlite db'

    def rowsCount(self, table):
        return len(self.query('SELECT * FROM ' + table))

    def columnsCount(self, table):
        return len(self.getColumnsNames(table))

    def addRow(self, values, table):

        try:
            self.query('INSERT INTO %s (%s) VALUES (%s)' % (table, ', '.join(self.getColumnsNames(table)), ', '.join(values)))

        except Exception as e:
            raise Exception('Invalid parameters /n' + e)

    def getColumnsNames(self, table):
        """
        return self.query("SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_SCHEMA`='" +
        table +
        "' AND `TABLE_NAME`=\'" +
        table +
        "\';")
        """

        return ['name','pswd']

    def save():
        self._cursor.commit()


    def getPswd(name):
        return self.query("SELECT pswd FROM accounts WHERE name='%s'" % (name))

    def query(self, query, void=False):

        ready = False

        self._cursor.execute(query)
        ready = True

        if not void and ready:

            results = self._cursor.fetchall()
            list = []

            if len(results) == 1:
                if len(results[0]) == 1:
                    return results[0][0]
                else:
                    for i in results[0]:
                        list.append(i)
            elif len(results) == 0:
                    return []
            else:
                for i in results:
                    if len(i) == 1:
                        list.append(i[0])
                    else:
                        sublist = []
                        for j in i:
                            sublist.append(j)
                        list.append(sublist)

            self.save()
            return list
