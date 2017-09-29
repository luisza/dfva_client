from client_fva.ui.managecontactsui import Ui_ManageContacts
from PyQt5 import QtWidgets


class ManageContacts(Ui_ManageContacts):

    def __init__(self, widget, main_app):
        Ui_ManageContacts.__init__(self)
        self.widget = widget
        self.main_app = main_app
        self.setupUi(widget)
