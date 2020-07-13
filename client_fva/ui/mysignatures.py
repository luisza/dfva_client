from client_fva.models.MySign import MySignModel
from client_fva.session_storage import SessionStorage
from client_fva.ui.mysignaturesui import Ui_MySignatures
from PyQt5 import QtWidgets


class MySignatures(Ui_MySignatures):

    def __init__(self, widget, main_app, db, index):
        Ui_MySignatures.__init__(self)
        self.db = db
        self.index = index
        self.widget = widget
        self.main_app = main_app
        self.setupUi(widget)
        storage = SessionStorage.getInstance()
        self.model_mysign = MySignModel(db=db, user=storage.users[index], tableview=self.mySignaturesTableView)
        self.initialize()

    def initialize(self):
        self.mySignaturesTableView.setModel(self.model_mysign)
        self.mySignaturesTableView.setSelectionMode(QtWidgets.QTableView.SingleSelection)
        self.mySignaturesTableView.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.model_mysign.refresh()