import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon


class FileChooser(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Seleccione un archivo'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Abrir archivo", "",
                                                  "All Files (*);;PDF (*.pdf)", options=options)

        return fileName
    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self, "Seleccione su archivo", "",
                                                "All Files (*);;Python Files (*.py)", options=options)
        return files

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "Seleccione su archivo", "",
                                                  "All Files (*);;Text Files (*.txt)", options=options)
        return fileName
