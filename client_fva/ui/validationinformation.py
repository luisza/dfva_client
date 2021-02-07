from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QTableWidgetItem

from .validationinformationui import Ui_Dialog


class ValidationInformation(QtWidgets.QDialog, Ui_Dialog):

    def __init__(self, widget, main_app):
        super().__init__(widget)
        Ui_Dialog.__init__(self)
        self.setupUi(self)
        self.signer_count = 0
        self.signers.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.signers.setRowCount(0)
        # set column count
        self.signers.setColumnCount(3)
        self.signers.setHorizontalHeaderItem(0, QTableWidgetItem("Identificación"))
        self.signers.setHorizontalHeaderItem(1, QTableWidgetItem("Nombre"))
        self.signers.setHorizontalHeaderItem(2, QTableWidgetItem("Fecha de firma"))
        
    def add_signer(self, identification, name, date):
        self.signers.insertRow(self.signers.rowCount())
        self.signers.setItem(self.signer_count, 0, QTableWidgetItem(identification))
        self.signers.setItem(self.signer_count, 1, QTableWidgetItem(name))
        self.signers.setItem(self.signer_count, 2, QTableWidgetItem(date))
        self.signer_count += 1
        self.signers.resizeColumnsToContents()

    def add_warning(self, text):
        self.warnings.addItem(text)

    def add_errors(self, text):
        self.errors.addItem(text)

    def set_status_icon(self, code):
        if code == 0:
            self.statusicon.setStyleSheet("image: url(:/images/connected.png);")
        else:
            self.statusicon.setStyleSheet("image: url(:/images/error.png);")