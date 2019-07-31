import sqlite3

class SqlUtils:

    def __init__(self, path):

        self._database = sqlite3.connect(path)
        self._cursor = self._database.cursor()

    def __repr__(self):
        return 'sqlite db'

    def save():
        self._cursor.commit()

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
