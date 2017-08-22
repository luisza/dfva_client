# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fvadialog.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FVADialog(object):
    def setupUi(self, FVADialog):
        FVADialog.setObjectName("FVADialog")
        FVADialog.resize(514, 289)
        self.formLayoutWidget = QtWidgets.QWidget(FVADialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(250, 90, 261, 95))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(11, 13, 11, 11)
        self.formLayout.setSpacing(6)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        self.label.setMinimumSize(QtCore.QSize(70, 0))
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.pin = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.pin.setInputMask("")
        self.pin.setText("")
        self.pin.setMaxLength(32767)
        self.pin.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pin.setObjectName("pin")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.pin)
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.code = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.code.setObjectName("code")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.code)
        self.label_3 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.displaytimeout = QtWidgets.QLCDNumber(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.displaytimeout.setFont(font)
        self.displaytimeout.setAutoFillBackground(False)
        self.displaytimeout.setStyleSheet("color:rgb(239, 41, 41)")
        self.displaytimeout.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.displaytimeout.setLineWidth(0)
        self.displaytimeout.setMidLineWidth(0)
        self.displaytimeout.setObjectName("displaytimeout")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.displaytimeout)
        self.requesting = QtWidgets.QLabel(FVADialog)
        self.requesting.setGeometry(QtCore.QRect(10, 230, 261, 21))
        self.requesting.setText("")
        self.requesting.setObjectName("requesting")
        self.information = QtWidgets.QLabel(FVADialog)
        self.information.setGeometry(QtCore.QRect(20, 10, 491, 51))
        self.information.setText("")
        self.information.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.information.setWordWrap(True)
        self.information.setObjectName("information")
        self.image = QtWidgets.QLabel(FVADialog)
        self.image.setGeometry(QtCore.QRect(20, 70, 181, 141))
        self.image.setText("")
        self.image.setObjectName("image")
        self.submit = QtWidgets.QPushButton(FVADialog)
        self.submit.setGeometry(QtCore.QRect(330, 260, 82, 23))
        self.submit.setObjectName("submit")
        self.cancel = QtWidgets.QPushButton(FVADialog)
        self.cancel.setGeometry(QtCore.QRect(420, 260, 82, 23))
        self.cancel.setObjectName("cancel")

        self.retranslateUi(FVADialog)
        QtCore.QMetaObject.connectSlotsByName(FVADialog)

    def retranslateUi(self, FVADialog):
        _translate = QtCore.QCoreApplication.translate
        FVADialog.setWindowTitle(_translate("FVADialog", "FVADialog"))
        self.label.setText(_translate("FVADialog", "Pin"))
        self.pin.setPlaceholderText(_translate("FVADialog", "Su pin"))
        self.label_2.setText(_translate("FVADialog", "Código"))
        self.label_3.setText(_translate("FVADialog", "Restante"))
        self.submit.setText(_translate("FVADialog", "Firmar"))
        self.cancel.setText(_translate("FVADialog", "Rechazar"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FVADialog = QtWidgets.QDialog()
    ui = Ui_FVADialog()
    ui.setupUi(FVADialog)
    FVADialog.show()
    sys.exit(app.exec_())

