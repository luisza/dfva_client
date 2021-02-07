from client_fva.ui.settingsui import Ui_Settings
from client_fva.ui.utils import apply_selected_appearance
from PyQt5 import QtWidgets


class Settings(Ui_Settings):

    def __init__(self, widget, main_app, fva_client_ui, user_settings):
        Ui_Settings.__init__(self)
        self.widget = widget
        self.setupUi(widget)
        self.main_app = main_app
        self.fva_client_ui = fva_client_ui
        self.theme.addItems(QtWidgets.QStyleFactory.keys())
        self.apply.clicked.connect(lambda: self.apply_selected_settings())
        self.cancel.clicked.connect(self.go_to_home)
        self.ok.clicked.connect(self.ok_settings)
        self.selectModulePath.clicked.connect(self.open_select_module_dialog)
        self.selectPathSaveDocs.clicked.connect(self.open_select_docs_path_dialog)
        self.user_settings = user_settings
        self.load_current_settings()

    def load_current_settings(self):
        # appearance
        self.theme.setCurrentText(self.user_settings.theme)
        self.fontSize.setValue(self.user_settings.font_size)
        self.fontComboBox.setCurrentText(self.user_settings.font_family)
        # security
        self.savePassword.setChecked(self.user_settings.save_password_in_manager)
        self.hideOnClose.setChecked(self.user_settings.hide_on_close)
        self.requestsBeforeError.setValue(self.user_settings.number_requests_before_fail)
        self.saveDocsPath.setText(self.user_settings.save_signed_docs_path)
        # module
        self.modulePath.setText(self.user_settings.module_path)

    def assign_selected_settings(self):
        # appearance
        self.user_settings.font_size = self.fontSize.value()
        self.user_settings.font_family = self.fontComboBox.currentText()
        self.user_settings.theme = self.theme.currentText()
        # security
        self.user_settings.save_password_in_manager = self.savePassword.isChecked()
        self.user_settings.hide_on_close = self.hideOnClose.isChecked()
        self.user_settings.number_requests_before_fail = self.requestsBeforeError.value()
        self.user_settings.save_signed_docs_path = self.saveDocsPath.text()
        # module
        self.user_settings.module_path = self.modulePath.text()

    def apply_selected_settings(self):
        self.assign_selected_settings()
        apply_selected_appearance(self.main_app, self.user_settings)
        self.user_settings.save()  # save applied settings to file

    def go_to_home(self):
        self.fva_client_ui.setup_tab_default_layout()

    def ok_settings(self):
        self.apply_selected_settings()
        self.go_to_home()

    def open_select_module_dialog(self):
        file_name, lib_type = QtWidgets.QFileDialog.getOpenFileName(self.fva_client_ui.main_window, "Seleccione Modulo",
                                                                    "", "Módulo Linux (*.so);; Módulo Mac (*.dylib);; "
                                                                    "Módulo Windows (*.dll)")
        if file_name:
            self.modulePath.setText(file_name)

    def open_select_docs_path_dialog(self):
        docs_path = QtWidgets.QFileDialog.getExistingDirectory(self.fva_client_ui.main_window, "Seleccione Directorio")
        if docs_path:
            self.saveDocsPath.setText(docs_path)
