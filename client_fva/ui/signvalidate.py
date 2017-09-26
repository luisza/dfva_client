from client_fva.ui.signvalidateui import Ui_SignValidate
from PyQt5 import QtWidgets


class SignValidate(Ui_SignValidate):

    def __init__(self, widget):
        Ui_SignValidate.__init__(self)
        self.widget = widget
        self.setupUi(widget)
