# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_elements/mysignatures.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MySignatures(object):
    def setupUi(self, MySignatures):
        MySignatures.setObjectName("MySignatures")
        MySignatures.resize(615, 371)
        MySignatures.setStyleSheet("color:rgb(76, 118, 82);\n"
"background-color:rgb(216, 230, 225);")
        self.mySignaturesLayout = QtWidgets.QVBoxLayout(MySignatures)
        self.mySignaturesLayout.setObjectName("mySignaturesLayout")
        self.titleLabel = QtWidgets.QLabel(MySignatures)
        self.titleLabel.setAcceptDrops(False)
        self.titleLabel.setStyleSheet("font: bold;")
        self.titleLabel.setScaledContents(True)
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setWordWrap(True)
        self.titleLabel.setObjectName("titleLabel")
        self.mySignaturesLayout.addWidget(self.titleLabel)
        self.mySignaturesTableView = QtWidgets.QTableView(MySignatures)
        self.mySignaturesTableView.setObjectName("mySignaturesTableView")
        self.mySignaturesLayout.addWidget(self.mySignaturesTableView)

        self.retranslateUi(MySignatures)
        QtCore.QMetaObject.connectSlotsByName(MySignatures)

    def retranslateUi(self, MySignatures):
        _translate = QtCore.QCoreApplication.translate
        MySignatures.setWindowTitle(_translate("MySignatures", "Mis Firmas"))
        self.titleLabel.setText(_translate("MySignatures", "Mis Firmas"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MySignatures = QtWidgets.QWidget()
    ui = Ui_MySignatures()
    ui.setupUi(MySignatures)
    MySignatures.show()
    sys.exit(app.exec_())

