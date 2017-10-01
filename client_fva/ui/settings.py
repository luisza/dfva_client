from client_fva.ui.settingsui import Ui_Settings
from PyQt5 import QtWidgets, QtGui


class Settings(Ui_Settings):

    def __init__(self, widget, main_app, fva_client_ui):
        Ui_Settings.__init__(self)
        self.widget = widget
        self.setupUi(widget)
        self.main_app = main_app
        self.fva_client_ui = fva_client_ui
        self.theme.addItems(QtWidgets.QStyleFactory.keys())
        self.apply.clicked.connect(lambda: self.applySettings())
        self.cancel.clicked.connect(self.goToHome)
        self.ok.clicked.connect(self.okSettings)

    def applySettings(self):
        self.main_app.setStyle(self.theme.currentText())  # apply theme
        font = '*{{font-size: {0}pt; font-family: "{1}";}}'.format(self.fontSize.value(), self.fontComboBox.currentText())
        # apply font size and family
        self.main_app.setStyleSheet(font)
        self.tabWidget.setStyleSheet(font)
        #

    def goToHome(self):
        self.fva_client_ui.setup_tab_default_layout()

    def okSettings(self):
        self.applySettings()
        self.goToHome()
