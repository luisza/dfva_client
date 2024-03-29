import sys

from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QInputDialog, QLineEdit

from client_fva.models.Pin import Secret
from client_fva.session_storage import SessionStorage
from client_fva.ui.fvaclientui import Ui_FVAClientUI
from client_fva.ui.myrequests import MyRequests
from client_fva.ui.mysignatures import MySignatures
from client_fva.ui.tab_manager import TabManager
from client_fva.ui.settings import Settings
from client_fva.ui.requestsignature import RequestSignature
from client_fva.ui.requestauthentication import RequestAuthentication
from client_fva.ui.signvalidate import SignValidate
from client_fva.ui.managecontacts import ManageContacts
from PyQt5 import QtWidgets, QtGui, QtCore
from client_fva.ui.tabdefault import TabDefault
from client_fva.user_settings import UserSettings
from client_fva.ui.utils import apply_selected_appearance
from client_fva.database import createDB
import logging

from client_fva.fva_logging import get_logging_window, configure_settings
from client_fva import signals

logger = logging.getLogger('dfva_client')
main_app = None
fva_client_ui = None
DEFAULT_TAB_INDEX = 0


class StatusBarManager(QObject):
    MAX_STEPS = 6
    hide = pyqtSignal()
    show = pyqtSignal()
    text = pyqtSignal(str)
    value = pyqtSignal(int)
    textbase = pyqtSignal(str)


    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.progressbar = QtWidgets.QProgressBar(controller.centralWidget)
        self.progressbar.setStyleSheet("")
        self.progressbar.setProperty("value", 0)
        self.progressbar.setOrientation(QtCore.Qt.Horizontal)
        self.progressbar.setInvertedAppearance(False)
        self.progressbar.setTextDirection(QtWidgets.QProgressBar.BottomToTop)
        self.controller.statusBar.addWidget(self.progressbar)
        self.start_process_bar()
        self.progressbar.hide()
        self.base_text = ''

        self.hide.connect(self.hide_fn)
        self.show.connect(self.show_fn)
        self.text.connect(self.text_fn)
        self.value.connect(self.value_fn)
        self.textbase.connect(self.basetext_fn)

    def start_process_bar(self):
        self.progressbar.setRange(0, self.MAX_STEPS)
        self.progressbar_status = 0
        self.progressbar.setValue(self.progressbar_status)
        self.operation_finished = False

    def end_process_bar(self):
        self.progressbar.setValue(self.MAX_STEPS)
        self.controller.statusBar.removeWidget(self.progressbar)
        self.operation_finished = True

    def hide_fn(self):
        self.progressbar.hide()

    def show_fn(self):
        self.progressbar.setFixedWidth(self.controller.centralWidget.width())
        self.progressbar.show()

    def basetext_fn(self, textdata):
        self.base_text = textdata

    def text_fn(self, textdata):
        self.progressbar.setFormat(self.base_text + textdata)

    def value_fn(self, val):
        self.progressbar.setValue(val)

class FVAClient(Ui_FVAClientUI):

    def __init__(self, main_window, usersettings=None):
        Ui_FVAClientUI.__init__(self)
        self.main_window = main_window
        self.setupUi(main_window)
        self.trayIcon = None
        self.trayIconOpenAction = None
        self.trayIconMenu = None
        self.trayIconExitAction = None
        self.setup_tray_icon()
        self.setup_tab_default_layout()
        self.set_enabled_specific_menu_actions(False)
        self.main_window.closeEvent = self.closeEvent
        self.actionExit.triggered.connect(self.main_window.close)
        self.actionMyRequests.triggered.connect(self.open_my_requests)
        self.actionMySignatures.triggered.connect(self.open_my_signatures)
        self.actionBitacoras.triggered.connect(self.open_logging_window)
        self.actionPreferences.triggered.connect(self.open_settings)
        self.actionRequestSignature.triggered.connect(self.open_request_signature)
        self.actionRequestAuthentication.triggered.connect(self.open_request_authentication)
        self.actionSignAuthenticate.triggered.connect(self.open_sign_validate)
        self.actionManageContacts.triggered.connect(self.open_manage_contacts)
        self.close_window = False  # by default window is only minimized
        self.force_exit = False  # the exit button was pressed (from the tray icon) so we need to exit it all
        self.db = None
        self.session_storage = SessionStorage.getInstance()
        self.session_storage.parent_widget = self.centralWidget
        self.main_thread = QtCore.QThread.currentThread()
        self.statusBarManager = StatusBarManager(self)

        # load initial app settings
        self.user_settings = usersettings
        apply_selected_appearance(main_app, self.user_settings)
        self.tabmanager = TabManager(self, main_app)
        signals.connect('pin', self.request_pin)
        signals.connect('notify', self.notify_user)

    def set_db(self, db):
        self.db = db
        self.session_storage.set_db(db)

    def closeEvent(self, event):
        # it will minimize or close it depending on what the user setup in their settings - if the user selected exit
        # from the tray icon then it will be closed no matter what
        self.close_window = not self.user_settings.hide_on_close
        if self.close_window or self.force_exit:
            event.accept()
            self.tabmanager.close()
        else:
            event.ignore()
            self.hide()

    def setup_tray_icon(self):
        self.trayIcon = QtWidgets.QSystemTrayIcon(QtGui.QIcon(":/images/icon.png"), self.main_window)
        self.trayIconMenu = QtWidgets.QMenu()
        self.trayIconOpenAction = self.trayIconMenu.addAction("Abrir")
        self.trayIconOpenAction.setIcon(QtGui.QIcon(":images/maximize.png"))
        self.trayIconOpenAction.triggered.connect(self.show)
        self.trayIconExitAction = self.trayIconMenu.addAction("Salir")
        self.trayIconExitAction.setIcon(QtGui.QIcon(":images/exit.png"))
        self.trayIconExitAction.triggered.connect(self.exit)
        self.trayIcon.setContextMenu(self.trayIconMenu)
        self.trayIcon.setToolTip("Cliente FVA")
        self.trayIcon.activated.connect(self.toggle)
        self.trayIcon.show()

    def setup_tab_layout(self, new_layout):
        if self.usrSlots.currentIndex() == DEFAULT_TAB_INDEX:
            QtWidgets.QMessageBox.information(self.usrSlots.currentWidget(), 'Seleccione Dispositivo',
                                              "Por favor seleccione una pestaña de dispositivo para acceder a "
                                              "esta opción.")
        else:
            tab = self.usrSlots.currentWidget()

            # cleans current tab layout so a new one can be assigned
            QtWidgets.QWidget().setLayout(tab.layout())
            tab.setLayout(new_layout)
            if self.session_storage.last_layout:
                if hasattr(self.session_storage.last_layout, 'disconnect'):
                    self.session_storage.last_layout.disconnect()
                    self.session_storage.last_layout = None

    def setup_tab_default_layout(self):
        tab = self.tab1
        self.usrSlots.setCurrentIndex(DEFAULT_TAB_INDEX)  # move to general tab
        # cleans the current tab layout and assigns the default one
        QtWidgets.QWidget().setLayout(tab.layout())
        tab_default = TabDefault(QtWidgets.QWidget(), main_app)
        tab.setLayout(tab_default.tabDefaultLayout)

    def show(self):
        self.main_window.show()

    def hide(self):
        self.main_window.hide()

    def exit(self):
        self.force_exit = True
        self.main_window.close()

    def toggle(self, reason):
        if reason == QtWidgets.QSystemTrayIcon.DoubleClick:
            if self.main_window.isVisible():
                self.hide()
            else:
                self.show()

    def get_serial_by_tabindex(self, index):
        serial = None
        for key in self.session_storage.session_info:
            if self.session_storage.session_info[key]['tabnumber'] == index:
                serial = key
                break
        return serial

    def open_my_requests(self):
        my_requests_ui = MyRequests(QtWidgets.QWidget(), main_app, self.db, self.get_serial_by_tabindex(self.usrSlots.currentIndex()))
        self.setup_tab_layout(my_requests_ui.myRequestsLayout)

    def open_my_signatures(self):
        my_signatures_ui = MySignatures(QtWidgets.QWidget(), main_app, self.db, self.get_serial_by_tabindex(self.usrSlots.currentIndex()))
        self.setup_tab_layout(my_signatures_ui.mySignaturesLayout)

    def open_settings(self):
        settings_dialog = QtWidgets.QDialog()  # settings will open on a new window
        settings_ui = Settings(settings_dialog, main_app, fva_client_ui, self.user_settings)
        settings_dialog.setLayout(settings_ui.settingsLayout)
        settings_dialog.show()

    def open_request_signature(self):
        request_signature_ui = RequestSignature(QtWidgets.QWidget(), main_app, self.db, self.get_serial_by_tabindex(self.usrSlots.currentIndex()))
        self.setup_tab_layout(request_signature_ui.requestSignatureLayout)
        self.session_storage.last_layout = request_signature_ui

    def open_request_authentication(self):
        request_authentication_ui = RequestAuthentication(QtWidgets.QWidget(), main_app, self.db,
                                                          self.get_serial_by_tabindex(self.usrSlots.currentIndex()))
        self.setup_tab_layout(request_authentication_ui.requestAuthenticationLayout)

    def open_sign_validate(self):
        sign_validate_ui = SignValidate(QtWidgets.QWidget(), main_app, self.get_serial_by_tabindex(self.usrSlots.currentIndex()))
        self.setup_tab_layout(sign_validate_ui.signValidateLayout)
        self.session_storage.last_layout = sign_validate_ui

    def open_manage_contacts(self):
        manage_contacts_ui = ManageContacts(QtWidgets.QWidget(), main_app, self.db,  self.get_serial_by_tabindex(self.usrSlots.currentIndex()))
        self.setup_tab_layout(manage_contacts_ui.manageContactsLayout)

    @staticmethod
    def open_logging_window():
        logging_window = get_logging_window()
        logging_window.show()
        logging_window.raise_()

    def set_enabled_specific_menu_actions(self, enabled):
        slot_specific_actions = [self.actionMySignatures, self.actionMyRequests, self.actionRequestSignature,
                                 self.actionRequestAuthentication, self.actionSignAuthenticate,
                                 self.actionManageContacts]
        for action in slot_specific_actions:
            action.setEnabled(enabled)

    def request_pin(self, sender, obj):
        serial = obj.data['serial']
        alias = self.session_storage.alias.filter(serial)
        alias_text = alias[0] if alias else serial
        text, ok = QInputDialog.getText(self.usrSlots.currentWidget(), "Atención", f"Ingrese su pin para {alias_text}",
                                        QLineEdit.Password)
        if ok and text:
            obj.response = {'pin': str(Secret(text)), 'serial': serial, 'rejected': False}
        else:
            obj.response = {'pin': "", 'serial': serial, 'rejected': True}
        signals.receive(obj, notify=True)

    def notify_user(self, sender, obj):
        if obj._type == signals.NOTIFTY_INFO:
            QtWidgets.QMessageBox.information(self.usrSlots.currentWidget(), 'Información Importante',
                                              obj.data['message'])
        elif obj._type == signals.NOTIFTY_ERROR:
            QtWidgets.QMessageBox.critical(self.usrSlots.currentWidget(), 'Error', obj.data['message'])
        elif obj._type == signals.NOTIFY_WARNING:
            QtWidgets.QMessageBox.warning(self.usrSlots.currentWidget(), 'Atención', obj.data['message'])
        signals.receive(obj, notify=True)


def run():
    global main_app
    main_app = QtWidgets.QApplication(sys.argv)
    global fva_client_ui
    user_settings = UserSettings.getInstance()
    user_settings.load()
    configure_settings(user_settings)
    fva_client_ui = FVAClient(QtWidgets.QMainWindow(), usersettings=user_settings)
    fva_client_ui.show()
    ok, db = createDB()
    fva_client_ui.set_db(db)
    if not ok:
        QtWidgets.QMessageBox.critical(None, "Error en la Base de Datos",
                                       "Hubo un problema cargando la base de datos, por favor intente más tarde o "
                                       "contacte un administrador.")
        sys.exit(1)
    sys.exit(main_app.exec_())
