from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi

from casket import CASKET
from casket.database import DbUtils
from casket.interface.IFirstSetup import IFirstSetup


class IMain(QMainWindow):

    def __init__(self):

        super().__init__()
        loadUi('casket/ui/main.ui', self)

        self.db = DbUtils()

        self.initialize_component()
        self.initialize_table()

        self.showMaximized()

        if CASKET.USER_CONFIG()["first_start"] == "none":

            setup = IFirstSetup()
            setup.exec_()

    def initialize_component(self):
        pass

    def initialize_table(self):

        columns_name = self.db.getColumnsNames('accounts')
        row = self.db.rowsCount('accounts')
        columns = self.db.columnsCount('accounts')

        while self.TBL_schema.rowCount() > 0:
            self.TBL_schema.removeRow(0)

        self.TBL_schema.setRowCount(row)
        self.TBL_schema.setColumnCount(columns)
        self.TBL_schema.setHorizontalHeaderLabels(columns_name)

        for i in range(0, row):
            for j in range(0, column):
                try:
                    widget.setItem(i, j, QTableWidgetItem(str(matrix[i][j]).replace('[', '').replace(']', '').replace('\'', '')))
                except Exception:
                    pass
