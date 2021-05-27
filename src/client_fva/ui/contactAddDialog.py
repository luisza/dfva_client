# -*- coding: utf-8 -*-

from client_fva.ui.contactAddDialogUI import Ui_AddContactDialog
from PyQt5.QtWidgets import QDialog


class AddContactDialog(QDialog, Ui_AddContactDialog):
    def __init__(self, parent=None):
        super(AddContactDialog, self).__init__(parent)
        self.setupUi(self)

    def setupUi(self, addContactDialog):
        super(AddContactDialog, self).setupUi(addContactDialog)
        self.dialogbox.accepted.connect(self.accept)
        self.dialogbox.rejected.connect(self.reject)

    @staticmethod
    def new_contact(parent=None):
        dialog = AddContactDialog(parent)
        result = dialog.exec_()

        return (dialog.firstname.text(),
                dialog.lastname.text(),
                dialog.identification.text(),
                result == QDialog.Accepted)
