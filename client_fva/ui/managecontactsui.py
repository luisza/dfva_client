# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'client_fva/ui/ui_elements/managecontacts.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
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
        self.contactsTableView = QtWidgets.QTableView(ManageContacts)
        self.contactsTableView.setObjectName("contactsTableView")
        self.manageContactsLayout.addWidget(self.contactsTableView, 3, 1, 1, 1)
        self.addContact = QtWidgets.QPushButton(ManageContacts)
        self.addContact.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.addContact.setStyleSheet("color: rgb(11, 35, 21);\n"
"background-color: rgb(229, 229, 229);")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addContact.setIcon(icon)
        self.addContact.setObjectName("addContact")
        self.manageContactsLayout.addWidget(self.addContact, 4, 1, 1, 1)
        self.searchContact = QtWidgets.QLineEdit(ManageContacts)
        self.searchContact.setObjectName("searchContact")
        self.manageContactsLayout.addWidget(self.searchContact, 1, 0, 1, 2)
        self.titleLabel_4 = QtWidgets.QLabel(ManageContacts)
        self.titleLabel_4.setStyleSheet("font: bold;")
        self.titleLabel_4.setScaledContents(True)
        self.titleLabel_4.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel_4.setWordWrap(True)
        self.titleLabel_4.setObjectName("titleLabel_4")
        self.manageContactsLayout.addWidget(self.titleLabel_4, 2, 1, 1, 1)
        self.titleLabel_3 = QtWidgets.QLabel(ManageContacts)
        self.titleLabel_3.setStyleSheet("font: bold;")
        self.titleLabel_3.setScaledContents(True)
        self.titleLabel_3.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel_3.setWordWrap(True)
        self.titleLabel_3.setObjectName("titleLabel_3")
        self.manageContactsLayout.addWidget(self.titleLabel_3, 2, 0, 1, 1)
        self.titleLabel_2 = QtWidgets.QLabel(ManageContacts)
        self.titleLabel_2.setStyleSheet("font: bold;")
        self.titleLabel_2.setScaledContents(True)
        self.titleLabel_2.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel_2.setWordWrap(True)
        self.titleLabel_2.setObjectName("titleLabel_2")
        self.manageContactsLayout.addWidget(self.titleLabel_2, 0, 0, 1, 2)
        self.addGroup = QtWidgets.QPushButton(ManageContacts)
        self.addGroup.setStyleSheet("color: rgb(11, 35, 21);\n"
"background-color: rgb(229, 229, 229);")
        self.addGroup.setIcon(icon)
        self.addGroup.setObjectName("addGroup")
        self.manageContactsLayout.addWidget(self.addGroup, 4, 0, 1, 1)
        self.groupsTableView = QtWidgets.QTableView(ManageContacts)
        self.groupsTableView.setObjectName("groupsTableView")
        self.manageContactsLayout.addWidget(self.groupsTableView, 3, 0, 1, 1)

        self.retranslateUi(ManageContacts)
        QtCore.QMetaObject.connectSlotsByName(ManageContacts)

    def retranslateUi(self, ManageContacts):
        _translate = QtCore.QCoreApplication.translate
        ManageContacts.setWindowTitle(_translate("ManageContacts", "Administrar Contactos"))
        self.addContact.setText(_translate("ManageContacts", "Contacto"))
        self.searchContact.setPlaceholderText(_translate("ManageContacts", "Buscar contacto..."))
        self.titleLabel_4.setText(_translate("ManageContacts", "Contactos"))
        self.titleLabel_3.setText(_translate("ManageContacts", "Grupos"))
        self.titleLabel_2.setText(_translate("ManageContacts", "Administrar Contactos"))
        self.addGroup.setText(_translate("ManageContacts", "Grupo"))

from . import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ManageContacts = QtWidgets.QWidget()
    ui = Ui_ManageContacts()
    ui.setupUi(ManageContacts)
    ManageContacts.show()
    sys.exit(app.exec_())

