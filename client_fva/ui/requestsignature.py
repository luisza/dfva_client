from client_fva.ui.requestsignatureui import Ui_RequestSignature
from PyQt5 import QtWidgets


class RequestSignature(Ui_RequestSignature):

    def __init__(self, widget, main_app):
        Ui_RequestSignature.__init__(self)
        self.widget = widget
        self.main_app = main_app
        self.setupUi(widget)
