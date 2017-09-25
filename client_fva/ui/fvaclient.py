import sys
from client_fva.ui.fvaclientui import Ui_FVAClientUI
from client_fva.ui.myrequests import MyRequests
from client_fva.ui.mysignatures import MySignatures
from client_fva.ui.tabdefault import TabDefault
from client_fva.ui.settings import Settings
from PyQt5 import QtWidgets, QtGui


class FVAClient(Ui_FVAClientUI):

    def __init__(self, main_window):
        Ui_FVAClientUI.__init__(self)
        self.main_window = main_window
        self.setupUi(main_window)
        self.setup_tab_default_layout()
        self.actionExit.triggered.connect(self.close)
        self.actionMyRequests.triggered.connect(self.open_my_requests)
        self.actionMySignatures.triggered.connect(self.open_my_signatures)
        self.actionPreferences.triggered.connect(self.open_settings)

    def setup_current_tab_layout(self, new_layout):
        tab = self.usrSlots.currentWidget()
        QtWidgets.QWidget().setLayout(tab.layout())  # cleans current tab layout so a new one can be assigned
        tab.setLayout(new_layout)

    def setup_tab_default_layout(self):
        tab_default = TabDefault(QtWidgets.QWidget())
        self.setup_current_tab_layout(tab_default.tabDefaultLayout)

    def start(self):
        self.main_window.show()

    def close(self, event):
        self.main_window.hide()

    def open_my_requests(self, event):
        my_requests_ui = MyRequests(QtWidgets.QWidget())
        self.setup_current_tab_layout(my_requests_ui.myRequestsLayout)

    def open_my_signatures(self, event):
        my_signatures_ui = MySignatures(QtWidgets.QWidget())
        self.setup_current_tab_layout(my_signatures_ui.mySignaturesLayout)

    def open_settings(self, event):
        settings_ui = Settings(QtWidgets.QWidget())
        self.setup_current_tab_layout(settings_ui.settingsLayout)


def run():
    app = QtWidgets.QApplication(sys.argv)
    fva_client_ui = FVAClient(QtWidgets.QMainWindow())
    fva_client_ui.start()
    sys.exit(app.exec_())
