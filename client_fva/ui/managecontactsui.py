# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_elements/managecontacts.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ManageContacts(object):
    def setupUi(self, ManageContacts):
        ManageContacts.setObjectName("ManageContacts")
        ManageContacts.resize(615, 371)
        ManageContacts.setStyleSheet("color:rgb(76, 118, 82);\n"
"background-color:rgb(216, 230, 225);")
        self.manageContactsLayout = QtWidgets.QGridLayout(ManageContacts)
        self.manageContactsLayout.setObjectName("manageContactsLayout")
        self.searchContact = QtWidgets.QLineEdit(ManageContacts)
        self.searchContact.setObjectName("searchContact")
        self.manageContactsLayout.addWidget(self.searchContact, 1, 0, 1, 1)
        self.addContact = QtWidgets.QPushButton(ManageContacts)
        self.addContact.setStyleSheet("color: rgb(11, 35, 21);\n"
"font: 75 9pt \"Noto Sans\";\n"
"background-color: rgb(229, 229, 229);")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addContact.setIcon(icon)
        self.addContact.setObjectName("addContact")
        self.manageContactsLayout.addWidget(self.addContact, 1, 1, 1, 1)
        self.contactsTableView = QtWidgets.QTableView(ManageContacts)
        self.contactsTableView.setObjectName("contactsTableView")
        self.manageContactsLayout.addWidget(self.contactsTableView, 2, 0, 1, 2)
        self.titleLabel = QtWidgets.QLabel(ManageContacts)
        self.titleLabel.setStyleSheet("font: 13pt;")
        self.titleLabel.setScaledContents(True)
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setWordWrap(True)
        self.titleLabel.setObjectName("titleLabel")
        self.manageContactsLayout.addWidget(self.titleLabel, 0, 0, 1, 2)

        self.retranslateUi(ManageContacts)
        QtCore.QMetaObject.connectSlotsByName(ManageContacts)

    def retranslateUi(self, ManageContacts):
        _translate = QtCore.QCoreApplication.translate
        ManageContacts.setWindowTitle(_translate("ManageContacts", "Administrar Contactos"))
        self.searchContact.setPlaceholderText(_translate("ManageContacts", "Buscar..."))
        self.addContact.setText(_translate("ManageContacts", "Contacto"))
        self.titleLabel.setText(_translate("ManageContacts", "Administrar Contactos"))

from . import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ManageContacts = QtWidgets.QWidget()
    ui = Ui_ManageContacts()
    ui.setupUi(ManageContacts)
    ManageContacts.show()
    sys.exit(app.exec_())

