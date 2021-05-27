# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'client_fva/ui/ui_elements/myrequests.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
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
        self.titleLabel.setStyleSheet("font: bold;")
        self.titleLabel.setScaledContents(True)
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setWordWrap(True)
        self.titleLabel.setObjectName("titleLabel")
        self.myRequestsLayout.addWidget(self.titleLabel)
        self.searchIdentification = QtWidgets.QLineEdit(MyRequests)
        self.searchIdentification.setObjectName("searchIdentification")
        self.myRequestsLayout.addWidget(self.searchIdentification)
        self.myRequests = QtWidgets.QTableWidget(MyRequests)
        self.myRequests.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.myRequests.setObjectName("myRequests")
        self.myRequests.setColumnCount(0)
        self.myRequests.setRowCount(0)
        self.myRequestsLayout.addWidget(self.myRequests)

        self.retranslateUi(MyRequests)
        QtCore.QMetaObject.connectSlotsByName(MyRequests)

    def retranslateUi(self, MyRequests):
        _translate = QtCore.QCoreApplication.translate
        MyRequests.setWindowTitle(_translate("MyRequests", "Mis Solicitudes"))
        self.titleLabel.setText(_translate("MyRequests", "Mis Solicitudes"))
        self.searchIdentification.setPlaceholderText(_translate("MyRequests", "Buscar identificación..."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MyRequests = QtWidgets.QWidget()
    ui = Ui_MyRequests()
    ui.setupUi(MyRequests)
    MyRequests.show()
    sys.exit(app.exec_())

