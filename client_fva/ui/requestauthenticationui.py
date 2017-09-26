# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_elements/requestauthentication.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_RequestAuthentication(object):
    def setupUi(self, RequestAuthentication):
        RequestAuthentication.setObjectName("RequestAuthentication")
        RequestAuthentication.resize(615, 371)
        RequestAuthentication.setStyleSheet("color:rgb(76, 118, 82);\n"
"background-color:rgb(216, 230, 225);")
        self.requestAuthenticationLayout = QtWidgets.QVBoxLayout(RequestAuthentication)
        self.requestAuthenticationLayout.setObjectName("requestAuthenticationLayout")
        self.titleLabel = QtWidgets.QLabel(RequestAuthentication)
        self.titleLabel.setAcceptDrops(False)
        self.titleLabel.setStyleSheet("font: 13pt;")
        self.titleLabel.setScaledContents(True)
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setWordWrap(True)
        self.titleLabel.setObjectName("titleLabel")
        self.requestAuthenticationLayout.addWidget(self.titleLabel)
        self.scrollArea = QtWidgets.QScrollArea(RequestAuthentication)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 595, 322))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollAreaLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.scrollAreaLayout.setObjectName("scrollAreaLayout")
        self.addContactFrame = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.addContactFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.addContactFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.addContactFrame.setMidLineWidth(0)
        self.addContactFrame.setObjectName("addContactFrame")
        self.addContactFrameLayout = QtWidgets.QGridLayout(self.addContactFrame)
        self.addContactFrameLayout.setObjectName("addContactFrameLayout")
        self.label = QtWidgets.QLabel(self.addContactFrame)
        self.label.setStyleSheet("font: 75 12pt \"Noto Sans\";\n"
"color: rgb(0, 0, 0);")
        self.label.setScaledContents(False)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label.setIndent(0)
        self.label.setObjectName("label")
        self.addContactFrameLayout.addWidget(self.label, 0, 0, 1, 1)
        self.contactsListWidget = QtWidgets.QListWidget(self.addContactFrame)
        self.contactsListWidget.setObjectName("contactsListWidget")
        self.addContactFrameLayout.addWidget(self.contactsListWidget, 2, 0, 1, 3)
        self.requestAuthentication = QtWidgets.QPushButton(self.addContactFrame)
        self.requestAuthentication.setEnabled(True)
        self.requestAuthentication.setSizeIncrement(QtCore.QSize(0, 0))
        self.requestAuthentication.setBaseSize(QtCore.QSize(0, 0))
        self.requestAuthentication.setStyleSheet("color: rgb(11, 35, 21);\n"
"font: 75 9pt \"Noto Sans\";\n"
"background-color: rgb(229, 229, 229);")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/send.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.requestAuthentication.setIcon(icon)
        self.requestAuthentication.setIconSize(QtCore.QSize(16, 16))
        self.requestAuthentication.setObjectName("requestAuthentication")
        self.addContactFrameLayout.addWidget(self.requestAuthentication, 3, 0, 1, 3)
        self.addContact = QtWidgets.QPushButton(self.addContactFrame)
        self.addContact.setAutoFillBackground(False)
        self.addContact.setStyleSheet("color: rgb(11, 35, 21);\n"
"font: 75 9pt \"Noto Sans\";\n"
"background-color: rgb(229, 229, 229);")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/images/add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addContact.setIcon(icon1)
        self.addContact.setObjectName("addContact")
        self.addContactFrameLayout.addWidget(self.addContact, 1, 2, 1, 1)
        self.searchContact = QtWidgets.QLineEdit(self.addContactFrame)
        self.searchContact.setObjectName("searchContact")
        self.addContactFrameLayout.addWidget(self.searchContact, 1, 0, 1, 1)
        self.scrollAreaLayout.addWidget(self.addContactFrame)
        self.requestAuthProgressBar = QtWidgets.QProgressBar(self.scrollAreaWidgetContents)
        self.requestAuthProgressBar.setProperty("value", 0)
        self.requestAuthProgressBar.setOrientation(QtCore.Qt.Horizontal)
        self.requestAuthProgressBar.setInvertedAppearance(False)
        self.requestAuthProgressBar.setTextDirection(QtWidgets.QProgressBar.BottomToTop)
        self.requestAuthProgressBar.setObjectName("requestAuthProgressBar")
        self.scrollAreaLayout.addWidget(self.requestAuthProgressBar)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.requestAuthenticationLayout.addWidget(self.scrollArea)

        self.retranslateUi(RequestAuthentication)
        QtCore.QMetaObject.connectSlotsByName(RequestAuthentication)

    def retranslateUi(self, RequestAuthentication):
        _translate = QtCore.QCoreApplication.translate
        RequestAuthentication.setWindowTitle(_translate("RequestAuthentication", "Solicitar Autenticación"))
        self.titleLabel.setText(_translate("RequestAuthentication", "Solicitar Autenticación"))
        self.label.setText(_translate("RequestAuthentication", "Seleccione Contacto"))
        self.requestAuthentication.setText(_translate("RequestAuthentication", "Solicitar"))
        self.addContact.setText(_translate("RequestAuthentication", "Contacto"))
        self.searchContact.setPlaceholderText(_translate("RequestAuthentication", "Buscar..."))
        self.requestAuthProgressBar.setFormat(_translate("RequestAuthentication", "Solicitando..."))

from . import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    RequestAuthentication = QtWidgets.QWidget()
    ui = Ui_RequestAuthentication()
    ui.setupUi(RequestAuthentication)
    RequestAuthentication.show()
    sys.exit(app.exec_())

