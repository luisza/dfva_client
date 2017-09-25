# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_elements/tabdefault.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TabDefault(object):
    def setupUi(self, TabDefault):
        TabDefault.setObjectName("TabDefault")
        TabDefault.resize(615, 371)
        TabDefault.setStyleSheet("color:rgb(76, 118, 82);\n"
"background-color:rgb(216, 230, 225);")
        self.tabDefaultLayout = QtWidgets.QGridLayout(TabDefault)
        self.tabDefaultLayout.setObjectName("tabDefaultLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 139, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.tabDefaultLayout.addItem(spacerItem, 0, 0, 1, 1)
        self.initialMessageLbl = QtWidgets.QLabel(TabDefault)
        self.initialMessageLbl.setStyleSheet("font: 13pt;")
        self.initialMessageLbl.setScaledContents(True)
        self.initialMessageLbl.setAlignment(QtCore.Qt.AlignCenter)
        self.initialMessageLbl.setWordWrap(True)
        self.initialMessageLbl.setObjectName("initialMessageLbl")
        self.tabDefaultLayout.addWidget(self.initialMessageLbl, 1, 0, 1, 2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 138, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.tabDefaultLayout.addItem(spacerItem1, 2, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(424, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.tabDefaultLayout.addItem(spacerItem2, 3, 0, 1, 1)
        self.refreshDevices = QtWidgets.QPushButton(TabDefault)
        self.refreshDevices.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.refreshDevices.setStyleSheet("color: rgb(11, 35, 21);\n"
"font: 75 9pt \"Noto Sans\";\n"
"background-color: rgb(229, 229, 229);\n"
"")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/refresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.refreshDevices.setIcon(icon)
        self.refreshDevices.setAutoDefault(False)
        self.refreshDevices.setDefault(False)
        self.refreshDevices.setFlat(False)
        self.refreshDevices.setObjectName("refreshDevices")
        self.tabDefaultLayout.addWidget(self.refreshDevices, 3, 1, 1, 1)

        self.retranslateUi(TabDefault)
        QtCore.QMetaObject.connectSlotsByName(TabDefault)

    def retranslateUi(self, TabDefault):
        _translate = QtCore.QCoreApplication.translate
        TabDefault.setWindowTitle(_translate("TabDefault", "Sin Dispositivo"))
        self.initialMessageLbl.setText(_translate("TabDefault", "Favor conecte su dispositivo de firma para comenzar."))
        self.refreshDevices.setText(_translate("TabDefault", "Refrescar Dispositivos"))

from . import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    TabDefault = QtWidgets.QWidget()
    ui = Ui_TabDefault()
    ui.setupUi(TabDefault)
    TabDefault.show()
    sys.exit(app.exec_())

