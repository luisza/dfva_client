# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'client_fva/ui/ui_elements/validationinformationcertificate.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(605, 441)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(260, 400, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.statusicon = QtWidgets.QLabel(Dialog)
        self.statusicon.setGeometry(QtCore.QRect(490, 30, 81, 41))
        self.statusicon.setStyleSheet("image: url(:/images/connecting.png);")
        self.statusicon.setText("")
        self.statusicon.setObjectName("statusicon")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(30, 50, 67, 19))
        self.label.setObjectName("label")
        self.status = QtWidgets.QLabel(Dialog)
        self.status.setGeometry(QtCore.QRect(100, 50, 301, 19))
        self.status.setText("")
        self.status.setObjectName("status")
        self.certinformation = QtWidgets.QTableWidget(Dialog)
        self.certinformation.setGeometry(QtCore.QRect(30, 120, 551, 261))
        self.certinformation.setObjectName("certinformation")
        self.certinformation.setColumnCount(0)
        self.certinformation.setRowCount(0)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Información del certificado"))
        self.label.setText(_translate("Dialog", "Estado:"))

from . import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

