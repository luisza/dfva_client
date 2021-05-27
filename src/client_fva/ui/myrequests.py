from client_fva.models.MyRequest import MyRequestModel
from client_fva.session_storage import SessionStorage
from client_fva.ui.myrequestsui import Ui_MyRequests
from PyQt5 import QtWidgets, QtGui


class MyRequests(Ui_MyRequests):

    def __init__(self, widget, main_app, db, serial):
        Ui_MyRequests.__init__(self)
        self.db = db
        self.widget = widget
        self.main_app = main_app
        self.setupUi(widget)
        self.session_storage = SessionStorage.getInstance()
        self.my_requests_model = MyRequestModel(db=self.db, user=self.session_storage.session_info[serial]['user'])
        self.initialize_and_populate_my_requests()
        self.searchIdentification.textChanged.connect(lambda x: self.search_requests(x))

    def fill_data(self, data_list):
        self.myRequests.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem("Identificación"))
        self.myRequests.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem("Tipo de Solicitud"))
        self.myRequests.setHorizontalHeaderItem(2, QtWidgets.QTableWidgetItem("Nombre de Documento"))
        self.myRequests.setHorizontalHeaderItem(3, QtWidgets.QTableWidgetItem("Ruta de Guardado"))
        self.myRequests.setHorizontalHeaderItem(4, QtWidgets.QTableWidgetItem("Estado"))
        count = 0
        for data in data_list:
            self.myRequests.insertRow(self.myRequests.rowCount())
            status = QtWidgets.QTableWidgetItem()
            if data[4] == 0:
                status.setIcon(QtGui.QIcon(":/images/connected.png"))
            else:
                status.setIcon(QtGui.QIcon(":/images/error.png"))
            status.setToolTip(data[5])
            self.myRequests.setItem(count, 0, QtWidgets.QTableWidgetItem(data[0]))
            self.myRequests.setItem(count, 1, QtWidgets.QTableWidgetItem(data[1]))
            self.myRequests.setItem(count, 2, QtWidgets.QTableWidgetItem(data[2]))
            self.myRequests.setItem(count, 3, QtWidgets.QTableWidgetItem(data[3]))
            self.myRequests.setItem(count, 4, status)
            count += 1

    def initialize_and_populate_my_requests(self):
        self.myRequests.setSelectionMode(QtWidgets.QTableView.SingleSelection)
        self.myRequests.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.myRequests.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # make it readonly
        self.myRequests.setRowCount(0)  # set row count
        self.myRequests.setColumnCount(5)  # set column count
        self.fill_data(self.my_requests_model.get_all())
        self.myRequests.resizeColumnsToContents()
        self.myRequests.horizontalHeader().setStretchLastSection(True)

    def search_requests(self, text):
        self.myRequests.clear()
        self.myRequests.setRowCount(0)
        if text:
            data = self.my_requests_model.filter(text)
        else:
            data = self.my_requests_model.get_all()
        self.fill_data(data)