# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_elements/requestsignature.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_RequestSignature(object):
    def setupUi(self, RequestSignature):
        RequestSignature.setObjectName("RequestSignature")
        RequestSignature.resize(618, 366)
        RequestSignature.setStyleSheet("color:rgb(76, 118, 82);\n"
"background-color:rgb(216, 230, 225);")
        self.requestSignatureLayout = QtWidgets.QGridLayout(RequestSignature)
        self.requestSignatureLayout.setObjectName("requestSignatureLayout")
        self.titleLabel = QtWidgets.QLabel(RequestSignature)
        self.titleLabel.setAcceptDrops(False)
        self.titleLabel.setStyleSheet("font: 13pt;")
        self.titleLabel.setScaledContents(True)
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setWordWrap(True)
        self.titleLabel.setObjectName("titleLabel")
        self.requestSignatureLayout.addWidget(self.titleLabel, 0, 0, 1, 1)
        self.scrollArea = QtWidgets.QScrollArea(RequestSignature)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.scrollArea.setMidLineWidth(0)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 598, 251))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollAreaLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.scrollAreaLayout.setObjectName("scrollAreaLayout")
        self.filesFrame = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.filesFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.filesFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.filesFrame.setMidLineWidth(0)
        self.filesFrame.setObjectName("filesFrame")
        self.filesFrameLayout = QtWidgets.QGridLayout(self.filesFrame)
        self.filesFrameLayout.setObjectName("filesFrameLayout")
        self.label = QtWidgets.QLabel(self.filesFrame)
        self.label.setStyleSheet("font: 75 10pt \"Noto Sans\";\n"
"color: rgb(0, 0, 0);")
        self.label.setScaledContents(False)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label.setIndent(0)
        self.label.setObjectName("label")
        self.filesFrameLayout.addWidget(self.label, 2, 0, 1, 1)
        self.filesWidget = QtWidgets.QListWidget(self.filesFrame)
        self.filesWidget.setAcceptDrops(True)
        self.filesWidget.setObjectName("filesWidget")
        self.filesFrameLayout.addWidget(self.filesWidget, 4, 0, 1, 3)
        self.browseFiles = QtWidgets.QPushButton(self.filesFrame)
        self.browseFiles.setAutoFillBackground(False)
        self.browseFiles.setStyleSheet("color: rgb(11, 35, 21);\n"
"font: 75 9pt \"Noto Sans\";\n"
"background-color: rgb(229, 229, 229);")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.browseFiles.setIcon(icon)
        self.browseFiles.setObjectName("browseFiles")
        self.filesFrameLayout.addWidget(self.browseFiles, 5, 2, 1, 1)
        self.scrollAreaLayout.addWidget(self.filesFrame, 0, 0, 1, 1)
        self.contactsFrame = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.contactsFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.contactsFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.contactsFrame.setMidLineWidth(0)
        self.contactsFrame.setObjectName("contactsFrame")
        self.contactsFrameLayout = QtWidgets.QGridLayout(self.contactsFrame)
        self.contactsFrameLayout.setObjectName("contactsFrameLayout")
        self.contactsListWidget = QtWidgets.QListWidget(self.contactsFrame)
        self.contactsListWidget.setObjectName("contactsListWidget")
        self.contactsFrameLayout.addWidget(self.contactsListWidget, 8, 0, 1, 3)
        self.searchContact = QtWidgets.QLineEdit(self.contactsFrame)
        self.searchContact.setText("")
        self.searchContact.setObjectName("searchContact")
        self.contactsFrameLayout.addWidget(self.searchContact, 4, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.contactsFrame)
        self.label_2.setStyleSheet("font: 75 10pt \"Noto Sans\";\n"
"color: rgb(0, 0, 0);")
        self.label_2.setScaledContents(False)
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_2.setIndent(0)
        self.label_2.setObjectName("label_2")
        self.contactsFrameLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.addContact = QtWidgets.QPushButton(self.contactsFrame)
        self.addContact.setAutoFillBackground(False)
        self.addContact.setStyleSheet("color: rgb(11, 35, 21);\n"
"font: 75 9pt \"Noto Sans\";\n"
"background-color: rgb(229, 229, 229);")
        self.addContact.setIcon(icon)
        self.addContact.setObjectName("addContact")
        self.contactsFrameLayout.addWidget(self.addContact, 4, 1, 1, 1)
        self.scrollAreaLayout.addWidget(self.contactsFrame, 0, 1, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.requestSignatureLayout.addWidget(self.scrollArea, 1, 0, 1, 1)
        self.requestSignature = QtWidgets.QPushButton(RequestSignature)
        self.requestSignature.setEnabled(True)
        self.requestSignature.setSizeIncrement(QtCore.QSize(0, 0))
        self.requestSignature.setBaseSize(QtCore.QSize(0, 0))
        self.requestSignature.setStyleSheet("color: rgb(11, 35, 21);\n"
"font: 75 9pt \"Noto Sans\";\n"
"background-color: rgb(229, 229, 229);")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/images/send.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.requestSignature.setIcon(icon1)
        self.requestSignature.setIconSize(QtCore.QSize(16, 16))
        self.requestSignature.setObjectName("requestSignature")
        self.requestSignatureLayout.addWidget(self.requestSignature, 3, 0, 1, 1)
        self.requestAuthProgressBar = QtWidgets.QProgressBar(RequestSignature)
        self.requestAuthProgressBar.setProperty("value", 0)
        self.requestAuthProgressBar.setOrientation(QtCore.Qt.Horizontal)
        self.requestAuthProgressBar.setInvertedAppearance(False)
        self.requestAuthProgressBar.setTextDirection(QtWidgets.QProgressBar.BottomToTop)
        self.requestAuthProgressBar.setObjectName("requestAuthProgressBar")
        self.requestSignatureLayout.addWidget(self.requestAuthProgressBar, 4, 0, 1, 1)

        self.retranslateUi(RequestSignature)
        QtCore.QMetaObject.connectSlotsByName(RequestSignature)

    def retranslateUi(self, RequestSignature):
        _translate = QtCore.QCoreApplication.translate
        RequestSignature.setWindowTitle(_translate("RequestSignature", "Solicitar Firma"))
        self.titleLabel.setText(_translate("RequestSignature", "Solicitar Firma"))
        self.label.setText(_translate("RequestSignature", "Archivo"))
        self.browseFiles.setText(_translate("RequestSignature", "Archivo"))
        self.searchContact.setPlaceholderText(_translate("RequestSignature", "Buscar..."))
        self.label_2.setText(_translate("RequestSignature", "Contacto"))
        self.addContact.setText(_translate("RequestSignature", "Contacto"))
        self.requestSignature.setText(_translate("RequestSignature", "Solicitar Firma"))
        self.requestAuthProgressBar.setFormat(_translate("RequestSignature", "Solicitando..."))

from . import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    RequestSignature = QtWidgets.QWidget()
    ui = Ui_RequestSignature()
    ui.setupUi(RequestSignature)
    RequestSignature.show()
    sys.exit(app.exec_())

