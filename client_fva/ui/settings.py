from client_fva.ui.settingsui import Ui_Settings
from PyQt5 import QtWidgets


class Settings(Ui_Settings):

    def __init__(self, widget):
        Ui_Settings.__init__(self)
        self.widget = widget
        self.setupUi(widget)
