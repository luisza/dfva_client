from client_fva.ui.tabdefaultui import Ui_TabDefault
from PyQt5 import QtWidgets


class TabDefault(Ui_TabDefault):

    def __init__(self, widget, main_app):
        Ui_TabDefault.__init__(self)
        self.widget = widget
        self.main_app = main_app
        self.setupUi(widget)
