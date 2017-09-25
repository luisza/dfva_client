from client_fva.ui.mysignaturesui import Ui_MySignatures
from PyQt5 import QtWidgets


class MySignatures(Ui_MySignatures):

    def __init__(self, widget):
        Ui_MySignatures.__init__(self)
        self.widget = widget
        self.setupUi(widget)
