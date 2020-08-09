
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QAbstractItemView

from client_fva.ui.filechooser import FileChooser
from client_fva.ui.requestsignatureui import Ui_RequestSignature


class RequestSignature(QWidget, Ui_RequestSignature):

    def __init__(self, widget, main_app):
        Ui_RequestSignature.__init__(self)
        super().__init__(widget)
        self.widget = widget
        self.main_app = main_app
        self.setupUi(widget)

        self.browseFiles.clicked.connect(self.get_document_path)
        self.filesWidget.set_parent(self)

    def add_file(self, path):
        self.filesWidget.addItem(path)

    @pyqtSlot(name='get_document_path')
    def get_document_path(self):

        d = FileChooser()
        path = d.openFileNameDialog()
        self.add_file(path)
        del d