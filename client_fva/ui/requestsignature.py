from client_fva.ui.requestsignatureui import Ui_RequestSignature
from PyQt5 import QtWidgets


class RequestSignature(Ui_RequestSignature):

    def __init__(self, widget):
        Ui_RequestSignature.__init__(self)
        self.widget = widget
        self.setupUi(widget)
