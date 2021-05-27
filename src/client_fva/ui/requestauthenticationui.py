# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'client_fva/ui/ui_elements/requestauthentication.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
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
        self.titleLabel.setStyleSheet("font: bold;")
        self.titleLabel.setScaledContents(True)
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setWordWrap(True)
        self.titleLabel.setObjectName("titleLabel")
        self.requestAuthenticationLayout.addWidget(self.titleLabel)
        self.scrollArea = QtWidgets.QScrollArea(RequestAuthentication)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 595, 326))
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
        self.label.setStyleSheet("color: rgb(0, 0, 0);\n"
"font: bold;")
        self.label.setScaledContents(False)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label.setIndent(0)
        self.label.setObjectName("label")
        self.addContactFrameLayout.addWidget(self.label, 0, 0, 1, 1)
        self.requestAuthentication = QtWidgets.QPushButton(self.addContactFrame)
        self.requestAuthentication.setEnabled(True)
        self.requestAuthentication.setSizeIncrement(QtCore.QSize(0, 0))
        self.requestAuthentication.setBaseSize(QtCore.QSize(0, 0))
        self.requestAuthentication.setStyleSheet("color: rgb(11, 35, 21);\n"
"background-color: rgb(229, 229, 229);")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/send.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.requestAuthentication.setIcon(icon)
        self.requestAuthentication.setIconSize(QtCore.QSize(16, 16))
        self.requestAuthentication.setObjectName("requestAuthentication")
        self.addContactFrameLayout.addWidget(self.requestAuthentication, 10, 0, 1, 2)
        self.searchContact = QtWidgets.QLineEdit(self.addContactFrame)
        self.searchContact.setObjectName("searchContact")
        self.addContactFrameLayout.addWidget(self.searchContact, 1, 0, 1, 1)
        self.add_contact = QtWidgets.QPushButton(self.addContactFrame)
        self.add_contact.setAutoFillBackground(False)
        self.add_contact.setStyleSheet("color: rgb(11, 35, 21);\n"
"background-color: rgb(229, 229, 229);")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/images/add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.add_contact.setIcon(icon1)
        self.add_contact.setObjectName("add_contact")
        self.addContactFrameLayout.addWidget(self.add_contact, 1, 1, 1, 1)
        self.contacts = QtWidgets.QTableWidget(self.addContactFrame)
        self.contacts.setObjectName("contacts")
        self.contacts.setColumnCount(0)
        self.contacts.setRowCount(0)
        self.addContactFrameLayout.addWidget(self.contacts, 3, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.cleanbtn = QtWidgets.QPushButton(self.addContactFrame)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/images/delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cleanbtn.setIcon(icon2)
        self.cleanbtn.setObjectName("cleanbtn")
        self.verticalLayout.addWidget(self.cleanbtn)
        self.addContactFrameLayout.addLayout(self.verticalLayout, 3, 1, 1, 1)
        self.contacts.raise_()
        self.label.raise_()
        self.requestAuthentication.raise_()
        self.add_contact.raise_()
        self.searchContact.raise_()
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
        self.label.setText(_translate("RequestAuthentication", "Seleccione Contacto o Ingrese Número de Identificación"))
        self.requestAuthentication.setText(_translate("RequestAuthentication", "Solicitar"))
        self.searchContact.setPlaceholderText(_translate("RequestAuthentication", "Buscar..."))
        self.add_contact.setText(_translate("RequestAuthentication", "Agregar"))
        self.cleanbtn.setText(_translate("RequestAuthentication", "Limpiar"))
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

