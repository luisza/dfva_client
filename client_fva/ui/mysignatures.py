from client_fva.ui.mysignaturesui import Ui_MySignatures
from PyQt5 import QtWidgets


class MySignatures(Ui_MySignatures):

    def __init__(self, widget, main_app):
        Ui_MySignatures.__init__(self)
        self.widget = widget
        self.main_app = main_app
        self.setupUi(widget)

