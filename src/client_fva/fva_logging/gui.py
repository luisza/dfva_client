from PyQt5 import QtWidgets, QtGui

from .core import Handler


class LoggingDialog(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resize(800, 600)
        self.setWindowTitle('Bitácora')
        self.setStyleSheet("color:rgb(76, 118, 82);background-color:rgb(216, 230, 225);")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.handler = Handler(self)
        log_text_box = QtWidgets.QPlainTextEdit(self)

        self.handler.new_record.connect(log_text_box.appendPlainText)
        layout = QtWidgets.QVBoxLayout()
        # Add the new logging box widget to the layout
        layout.addWidget(log_text_box)
        self.setLayout(layout)
