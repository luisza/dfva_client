from client_fva.ui.requestauthenticationui import Ui_RequestAuthentication
from PyQt5 import QtWidgets


class RequestAuthentication(Ui_RequestAuthentication):

    def __init__(self, widget):
        Ui_RequestAuthentication.__init__(self)
        self.widget = widget
        self.setupUi(widget)
