# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'client_fva/ui/ui_elements/contactAddDialog.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AddContactDialog(object):
    def setupUi(self, AddContactDialog):
        AddContactDialog.setObjectName("AddContactDialog")
        AddContactDialog.resize(495, 265)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        AddContactDialog.setWindowIcon(icon)
        self.dialogbox = QtWidgets.QDialogButtonBox(AddContactDialog)
        self.dialogbox.setGeometry(QtCore.QRect(280, 230, 166, 23))
        self.dialogbox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.dialogbox.setObjectName("dialogbox")
        self.formLayoutWidget = QtWidgets.QWidget(AddContactDialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(20, 30, 451, 181))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(11, 11, 11, 11)
        self.formLayout.setHorizontalSpacing(50)
        self.formLayout.setVerticalSpacing(25)
        self.formLayout.setObjectName("formLayout")
        self.label_firstname = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_firstname.setObjectName("label_firstname")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_firstname)
        self.firstname = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.firstname.setObjectName("firstname")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.firstname)
        self.label_lastname = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_lastname.setObjectName("label_lastname")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_lastname)
        self.lastname = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lastname.setObjectName("lastname")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lastname)
        self.label_identification = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_identification.setObjectName("label_identification")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_identification)
        self.identification = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.identification.setObjectName("identification")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.identification)

        self.retranslateUi(AddContactDialog)
        QtCore.QMetaObject.connectSlotsByName(AddContactDialog)

    def retranslateUi(self, AddContactDialog):
        _translate = QtCore.QCoreApplication.translate
        AddContactDialog.setWindowTitle(_translate("AddContactDialog", "Agregar Contacto"))
        self.label_firstname.setText(_translate("AddContactDialog", "Nombre"))
        self.label_lastname.setText(_translate("AddContactDialog", "Apellidos"))
        self.label_identification.setText(_translate("AddContactDialog", "Identificación"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AddContactDialog = QtWidgets.QDialog()
    ui = Ui_AddContactDialog()
    ui.setupUi(AddContactDialog)
    AddContactDialog.show()
    sys.exit(app.exec_())

