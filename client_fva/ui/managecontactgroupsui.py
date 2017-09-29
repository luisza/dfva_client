# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_elements/managecontactgroups.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ManageContactGroups(object):
    def setupUi(self, ManageContactGroups):
        ManageContactGroups.setObjectName("ManageContactGroups")
        ManageContactGroups.resize(615, 371)
        ManageContactGroups.setStyleSheet("color:rgb(76, 118, 82);\n"
"background-color:rgb(216, 230, 225);")
        self.manageContactGroupsLayout = QtWidgets.QGridLayout(ManageContactGroups)
        self.manageContactGroupsLayout.setObjectName("manageContactGroupsLayout")
        self.searchContact = QtWidgets.QLineEdit(ManageContactGroups)
        self.searchContact.setObjectName("searchContact")
        self.manageContactGroupsLayout.addWidget(self.searchContact, 1, 0, 1, 1)
        self.addContactGroup = QtWidgets.QPushButton(ManageContactGroups)
        self.addContactGroup.setStyleSheet("color: rgb(11, 35, 21);\n"
"background-color: rgb(229, 229, 229);")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addContactGroup.setIcon(icon)
        self.addContactGroup.setObjectName("addContactGroup")
        self.manageContactGroupsLayout.addWidget(self.addContactGroup, 1, 1, 1, 1)
        self.contactGroupsTreeView = QtWidgets.QTreeView(ManageContactGroups)
        self.contactGroupsTreeView.setObjectName("contactGroupsTreeView")
        self.manageContactGroupsLayout.addWidget(self.contactGroupsTreeView, 2, 0, 1, 2)
        self.titleLabel = QtWidgets.QLabel(ManageContactGroups)
        self.titleLabel.setStyleSheet("font: bold;")
        self.titleLabel.setScaledContents(True)
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setWordWrap(True)
        self.titleLabel.setObjectName("titleLabel")
        self.manageContactGroupsLayout.addWidget(self.titleLabel, 0, 0, 1, 2)

        self.retranslateUi(ManageContactGroups)
        QtCore.QMetaObject.connectSlotsByName(ManageContactGroups)

    def retranslateUi(self, ManageContactGroups):
        _translate = QtCore.QCoreApplication.translate
        ManageContactGroups.setWindowTitle(_translate("ManageContactGroups", "Administrar Grupos"))
        self.searchContact.setPlaceholderText(_translate("ManageContactGroups", "Buscar..."))
        self.addContactGroup.setText(_translate("ManageContactGroups", "Grupo"))
        self.titleLabel.setText(_translate("ManageContactGroups", "Administrar Grupos"))

from . import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ManageContactGroups = QtWidgets.QWidget()
    ui = Ui_ManageContactGroups()
    ui.setupUi(ManageContactGroups)
    ManageContactGroups.show()
    sys.exit(app.exec_())

