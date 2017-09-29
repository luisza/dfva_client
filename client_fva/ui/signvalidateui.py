# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_elements/signvalidate.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SignValidate(object):
    def setupUi(self, SignValidate):
        SignValidate.setObjectName("SignValidate")
        SignValidate.resize(618, 366)
        SignValidate.setStyleSheet("color:rgb(76, 118, 82);\n"
"background-color:rgb(216, 230, 225);")
        self.signValidateLayout = QtWidgets.QGridLayout(SignValidate)
        self.signValidateLayout.setObjectName("signValidateLayout")
        self.titleLabel = QtWidgets.QLabel(SignValidate)
        self.titleLabel.setAcceptDrops(False)
        self.titleLabel.setStyleSheet("font: bold;")
        self.titleLabel.setScaledContents(True)
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setWordWrap(True)
        self.titleLabel.setObjectName("titleLabel")
        self.signValidateLayout.addWidget(self.titleLabel, 0, 0, 1, 3)
        self.scrollArea = QtWidgets.QScrollArea(SignValidate)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.scrollArea.setMidLineWidth(0)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 598, 286))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollAreaWidgetLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.scrollAreaWidgetLayout.setObjectName("scrollAreaWidgetLayout")
        self.fileFrame = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.fileFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.fileFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.fileFrame.setMidLineWidth(0)
        self.fileFrame.setObjectName("fileFrame")
        self.fileFrameLayout = QtWidgets.QGridLayout(self.fileFrame)
        self.fileFrameLayout.setObjectName("fileFrameLayout")
        self.label = QtWidgets.QLabel(self.fileFrame)
        self.label.setStyleSheet("font: bold;\n"
"color: rgb(0, 0, 0);")
        self.label.setScaledContents(False)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label.setIndent(0)
        self.label.setObjectName("label")
        self.fileFrameLayout.addWidget(self.label, 0, 0, 1, 1)
        self.filesWidget = QtWidgets.QListWidget(self.fileFrame)
        self.filesWidget.setAcceptDrops(True)
        self.filesWidget.setObjectName("filesWidget")
        self.fileFrameLayout.addWidget(self.filesWidget, 5, 0, 1, 4)
        spacerItem = QtWidgets.QSpacerItem(40, 3, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.fileFrameLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.browseFiles = QtWidgets.QPushButton(self.fileFrame)
        self.browseFiles.setAutoFillBackground(False)
        self.browseFiles.setStyleSheet("color: rgb(11, 35, 21);\n"
"background-color: rgb(229, 229, 229);")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.browseFiles.setIcon(icon)
        self.browseFiles.setObjectName("browseFiles")
        self.fileFrameLayout.addWidget(self.browseFiles, 0, 3, 1, 1)
        self.sign = QtWidgets.QPushButton(self.fileFrame)
        self.sign.setEnabled(True)
        self.sign.setSizeIncrement(QtCore.QSize(0, 0))
        self.sign.setBaseSize(QtCore.QSize(0, 0))
        self.sign.setStyleSheet("color: rgb(11, 35, 21);\n"
"background-color: rgb(229, 229, 229);")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/images/sign.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.sign.setIcon(icon1)
        self.sign.setIconSize(QtCore.QSize(16, 16))
        self.sign.setObjectName("sign")
        self.fileFrameLayout.addWidget(self.sign, 7, 3, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.fileFrameLayout.addItem(spacerItem1, 7, 1, 1, 1)
        self.validate = QtWidgets.QPushButton(self.fileFrame)
        self.validate.setEnabled(True)
        self.validate.setSizeIncrement(QtCore.QSize(0, 0))
        self.validate.setBaseSize(QtCore.QSize(0, 0))
        self.validate.setStyleSheet("color: rgb(11, 35, 21);\n"
"background-color: rgb(229, 229, 229);")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/images/validate.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.validate.setIcon(icon2)
        self.validate.setIconSize(QtCore.QSize(16, 16))
        self.validate.setObjectName("validate")
        self.fileFrameLayout.addWidget(self.validate, 7, 2, 1, 1)
        self.scrollAreaWidgetLayout.addWidget(self.fileFrame, 1, 1, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.signValidateLayout.addWidget(self.scrollArea, 4, 0, 1, 3)
        self.signValidateProgressBar = QtWidgets.QProgressBar(SignValidate)
        self.signValidateProgressBar.setStyleSheet("")
        self.signValidateProgressBar.setProperty("value", 0)
        self.signValidateProgressBar.setOrientation(QtCore.Qt.Horizontal)
        self.signValidateProgressBar.setInvertedAppearance(False)
        self.signValidateProgressBar.setTextDirection(QtWidgets.QProgressBar.BottomToTop)
        self.signValidateProgressBar.setObjectName("signValidateProgressBar")
        self.signValidateLayout.addWidget(self.signValidateProgressBar, 9, 0, 1, 3)

        self.retranslateUi(SignValidate)
        QtCore.QMetaObject.connectSlotsByName(SignValidate)

    def retranslateUi(self, SignValidate):
        _translate = QtCore.QCoreApplication.translate
        SignValidate.setWindowTitle(_translate("SignValidate", "Firmar - Validar Documentos"))
        self.titleLabel.setText(_translate("SignValidate", "Firmar - Validar Documentos"))
        self.label.setText(_translate("SignValidate", "Archivo"))
        self.browseFiles.setText(_translate("SignValidate", "Archivo"))
        self.sign.setText(_translate("SignValidate", "Firmar"))
        self.validate.setText(_translate("SignValidate", "Validar"))
        self.signValidateProgressBar.setFormat(_translate("SignValidate", "Procesando..."))

from . import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SignValidate = QtWidgets.QWidget()
    ui = Ui_SignValidate()
    ui.setupUi(SignValidate)
    SignValidate.show()
    sys.exit(app.exec_())

