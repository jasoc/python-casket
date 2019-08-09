from PyQt5.QtWidgets import QMainWindow, QTableWidget, QHeaderView
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi

import Casket
from Casket.database import DbUtils
from Casket.interface.IFirstSetup import IFirstSetup


class IMain(QMainWindow):

    def __init__(self):

        super().__init__()
        loadUi('Casket/ui/main.ui', self)

        self.db = DbUtils()

        self.initialize_component()
        self.initialize_table()

        self.showMaximized()

        if Casket.FIRST_START():

            setup = IFirstSetup()
            setup.exec_()

    def initialize_component(self):

        self.TBL_schema.setEditTriggers(QTableWidget.NoEditTriggers)
        self.TBL_schema.horizontalHeader().setStretchLastSection(True)
        self.TBL_schema.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

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
