from client_fva.ui.myrequestsui import Ui_MyRequests
from PyQt5 import QtWidgets


class MyRequests(Ui_MyRequests):

    def __init__(self, widget, main_app):
        Ui_MyRequests.__init__(self)
        self.widget = widget
        self.main_app = main_app
        self.setupUi(widget)

