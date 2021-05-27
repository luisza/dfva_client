from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QTableWidgetItem

from .validationinformationcertificateui import Ui_Dialog


class ValidationInformationCertificate(QtWidgets.QDialog, Ui_Dialog):

    def __init__(self, widget, main_app):
        super().__init__(widget)
        Ui_Dialog.__init__(self)
        self.setupUi(self)
        self.signer_count = 0
        self.certinformation.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.certinformation.setRowCount(0)
        # set column count
        self.certinformation.setColumnCount(4)
        self.certinformation.setHorizontalHeaderItem(0, QTableWidgetItem("Identificación"))
        self.certinformation.setHorizontalHeaderItem(1, QTableWidgetItem("Nombre"))
        self.certinformation.setHorizontalHeaderItem(2, QTableWidgetItem("Válido desde"))
        self.certinformation.setHorizontalHeaderItem(3, QTableWidgetItem("Válido hasta"))
        self.certinformation.resizeColumnsToContents()

    def add_owner(self, data):

        # ('status', 'status_text', 'was_successfully', 'identification', 'full_name', 'start_validity', 'end_validity' )
        if data['was_successfully']:
            self.certinformation.insertRow(self.certinformation.rowCount())
            self.certinformation.setItem(self.signer_count, 0, QTableWidgetItem(data['identification']))
            self.certinformation.setItem(self.signer_count, 1, QTableWidgetItem(data['full_name']))
            self.certinformation.setItem(self.signer_count, 2, QTableWidgetItem(data['start_validity']))
            self.certinformation.setItem(self.signer_count, 3, QTableWidgetItem(data['end_validity']))
            self.signer_count += 1
            self.certinformation.resizeColumnsToContents()

    def set_status_icon(self, code):
        if code:
            self.statusicon.setStyleSheet("image: url(:/images/connected.png);")
        else:
            self.statusicon.setStyleSheet("image: url(:/images/error.png);")