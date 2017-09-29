from client_fva.ui.requestauthenticationui import Ui_RequestAuthentication
from PyQt5 import QtWidgets


class RequestAuthentication(Ui_RequestAuthentication):

    def __init__(self, widget, main_app):
        Ui_RequestAuthentication.__init__(self)
        self.widget = widget
        self.main_app = main_app
        self.setupUi(widget)
