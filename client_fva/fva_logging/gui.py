from PyQt5 import QtCore, QtWidgets
import logging

from .core import Handler

class LoggingDialog(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resize(800, 600)
        self.handler = Handler(self)
        log_text_box = QtWidgets.QPlainTextEdit(self)

        logging.getLogger().addHandler(self.handler)
        logging.getLogger().setLevel(logging.INFO)
        self.handler.new_record.connect(log_text_box.appendPlainText)
        layout = QtWidgets.QVBoxLayout()
        # Add the new logging box widget to the layout
        layout.addWidget(log_text_box)
        self.setLayout(layout)