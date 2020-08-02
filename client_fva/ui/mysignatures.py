from PyQt5.QtWidgets import QTableWidgetItem

from client_fva.models.MySign import MySignModel
from client_fva.session_storage import SessionStorage
from client_fva.ui.mysignaturesui import Ui_MySignatures
from PyQt5 import QtWidgets, QtGui


class MySignatures(Ui_MySignatures):

    def __init__(self, widget, main_app, db, index):
        Ui_MySignatures.__init__(self)
        self.db = db
        self.widget = widget
        self.main_app = main_app
        self.setupUi(widget)
        storage = SessionStorage.getInstance()
        self.my_signatures_model = MySignModel(db=db, user=storage.users[index], tableview=self.mySignatures)
        self.initialize_and_populate_my_signatures()
        self.searchDocument.textChanged.connect(lambda x: self.search_documents(x))

    def fill_data(self, data_list):
        self.mySignatures.setHorizontalHeaderItem(0, QTableWidgetItem("Nombre"))
        self.mySignatures.setHorizontalHeaderItem(1, QTableWidgetItem("Ruta de guardado"))
        self.mySignatures.setHorizontalHeaderItem(2, QTableWidgetItem("Estado"))
        count = 0
        for data in data_list:
            self.mySignatures.insertRow(self.mySignatures.rowCount())
            status = QTableWidgetItem()
            if data[2] == 0:
                status.setIcon(QtGui.QIcon(":/images/connected.png"))
            else:
                status.setIcon(QtGui.QIcon(":/images/error.png"))
            status.setToolTip(data[3])
            self.mySignatures.setItem(count, 0, QTableWidgetItem(data[0]))
            self.mySignatures.setItem(count, 1, QTableWidgetItem(data[1]))
            self.mySignatures.setItem(count, 2, status)
            count += 1

    def initialize_and_populate_my_signatures(self):
        self.mySignatures.setSelectionMode(QtWidgets.QTableView.SingleSelection)
        self.mySignatures.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.mySignatures.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # make it readonly
        self.mySignatures.setRowCount(0)  # set row count
        self.mySignatures.setColumnCount(3)  # set column count
        self.fill_data(self.my_signatures_model.get_all())
        self.mySignatures.resizeColumnsToContents()
        self.mySignatures.horizontalHeader().setStretchLastSection(True)

    def search_documents(self, text):
        self.mySignatures.clear()
        self.mySignatures.setRowCount(0)
        if text:
            data = self.my_signatures_model.filter(text)
        else:
            data = self.my_signatures_model.get_all()
        self.fill_data(data)
