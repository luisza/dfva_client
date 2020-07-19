# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'client_fva/ui/ui_elements/validationinformation.ui'
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
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setGeometry(QtCore.QRect(6, 19, 591, 371))
        self.tabWidget.setObjectName("tabWidget")
        self.information = QtWidgets.QWidget()
        self.information.setObjectName("information")
        self.label_2 = QtWidgets.QLabel(self.information)
        self.label_2.setGeometry(QtCore.QRect(10, 20, 67, 19))
        self.label_2.setObjectName("label_2")
        self.label = QtWidgets.QLabel(self.information)
        self.label.setGeometry(QtCore.QRect(10, 50, 81, 19))
        self.label.setObjectName("label")
        self.status = QtWidgets.QLabel(self.information)
        self.status.setGeometry(QtCore.QRect(90, 20, 301, 19))
        self.status.setObjectName("status")
        self.signers = QtWidgets.QTableWidget(self.information)
        self.signers.setGeometry(QtCore.QRect(10, 80, 561, 241))
        self.signers.setTextElideMode(QtCore.Qt.ElideNone)
        self.signers.setObjectName("signers")
        self.signers.setColumnCount(0)
        self.signers.setRowCount(0)
        self.statusicon = QtWidgets.QLabel(self.information)
        self.statusicon.setGeometry(QtCore.QRect(500, 10, 81, 41))
        self.statusicon.setStyleSheet("image: url(:/images/connecting.png);")
        self.statusicon.setText("")
        self.statusicon.setObjectName("statusicon")
        self.tabWidget.addTab(self.information, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.label_4 = QtWidgets.QLabel(self.tab_2)
        self.label_4.setGeometry(QtCore.QRect(10, 10, 231, 19))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.tab_2)
        self.label_5.setGeometry(QtCore.QRect(10, 150, 67, 19))
        self.label_5.setObjectName("label_5")
        self.warnings = QtWidgets.QListWidget(self.tab_2)
        self.warnings.setGeometry(QtCore.QRect(10, 30, 561, 111))
        self.warnings.setObjectName("warnings")
        self.errors = QtWidgets.QListWidget(self.tab_2)
        self.errors.setGeometry(QtCore.QRect(10, 180, 561, 151))
        self.errors.setObjectName("errors")
        self.tabWidget.addTab(self.tab_2, "")

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        self.buttonBox.accepted.connect(Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Información del documento"))
        self.label_2.setText(_translate("Dialog", "Estado:"))
        self.label.setText(_translate("Dialog", "Firmantes:"))
        self.status.setText(_translate("Dialog", "Información de estado de la validación"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.information), _translate("Dialog", "Información de firma"))
        self.label_4.setText(_translate("Dialog", "Advertencias"))
        self.label_5.setText(_translate("Dialog", "Errores"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "Advertencias y errores"))

from . import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

