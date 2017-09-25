# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_elements/myrequests.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MyRequests(object):
    def setupUi(self, MyRequests):
        MyRequests.setObjectName("MyRequests")
        MyRequests.resize(615, 371)
        MyRequests.setStyleSheet("color:rgb(76, 118, 82);\n"
"background-color:rgb(216, 230, 225);")
        self.myRequestsLayout = QtWidgets.QVBoxLayout(MyRequests)
        self.myRequestsLayout.setObjectName("myRequestsLayout")
        self.titleLabel = QtWidgets.QLabel(MyRequests)
        self.titleLabel.setStyleSheet("font: 13pt;")
        self.titleLabel.setScaledContents(True)
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setWordWrap(True)
        self.titleLabel.setObjectName("titleLabel")
        self.myRequestsLayout.addWidget(self.titleLabel)
        self.myRequestsTableView = QtWidgets.QTableView(MyRequests)
        self.myRequestsTableView.setObjectName("myRequestsTableView")
        self.myRequestsLayout.addWidget(self.myRequestsTableView)

        self.retranslateUi(MyRequests)
        QtCore.QMetaObject.connectSlotsByName(MyRequests)

    def retranslateUi(self, MyRequests):
        _translate = QtCore.QCoreApplication.translate
        MyRequests.setWindowTitle(_translate("MyRequests", "Mis Solicitudes"))
        self.titleLabel.setText(_translate("MyRequests", "Mis Solicitudes"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MyRequests = QtWidgets.QWidget()
    ui = Ui_MyRequests()
    ui.setupUi(MyRequests)
    MyRequests.show()
    sys.exit(app.exec_())

