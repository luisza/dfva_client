from client_fva.ui.tabDefaultui import Ui_TabDefault
from PyQt5 import QtWidgets


class TabDefault(Ui_TabDefault):

    def __init__(self, widget):
        Ui_TabDefault.__init__(self)
        self.widget = widget
        self.setupUi(widget)
