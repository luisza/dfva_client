from client_fva.ui.managecontactgroupsui import Ui_ManageContactGroups
from PyQt5 import QtWidgets


class ManageContactGroups(Ui_ManageContactGroups):

    def __init__(self, widget):
        Ui_ManageContactGroups.__init__(self)
        self.widget = widget
        self.setupUi(widget)
