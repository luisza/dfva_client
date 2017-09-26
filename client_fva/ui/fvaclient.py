import sys
from client_fva.ui.fvaclientui import Ui_FVAClientUI
from client_fva.ui.myrequests import MyRequests
from client_fva.ui.mysignatures import MySignatures
from client_fva.ui.tabdefault import TabDefault
from client_fva.ui.settings import Settings
from client_fva.ui.requestsignature import RequestSignature
from client_fva.ui.requestauthentication import RequestAuthentication
from client_fva.ui.signvalidate import SignValidate
from client_fva.ui.managecontacts import ManageContacts
from client_fva.ui.managecontactgroups import ManageContactGroups
from PyQt5 import QtWidgets, QtGui


class FVAClient(Ui_FVAClientUI):

    def __init__(self, main_window):
        Ui_FVAClientUI.__init__(self)
        self.main_window = main_window
        self.setupUi(main_window)
        self.setup_tray_icon()
        self.setup_tab_default_layout()
        self.main_window.closeEvent = self.closeEvent
        self.actionExit.triggered.connect(self.hide)
        self.actionMyRequests.triggered.connect(self.open_my_requests)
        self.actionMySignatures.triggered.connect(self.open_my_signatures)
        self.actionPreferences.triggered.connect(self.open_settings)
        self.actionRequestSignature.triggered.connect(self.open_request_signature)
        self.actionRequestAuthentication.triggered.connect(self.open_request_authentication)
        self.actionSignAuthenticate.triggered.connect(self.open_sign_validate)
        self.actionManageContacts.triggered.connect(self.open_manage_contacts)
        self.actionManageGroups.triggered.connect(self.open_manage_contact_groups)

        self.close_window = False  # by default window is only minimized

    def closeEvent(self, event):
        if self.close_window:
            event.accept()
        else:
            event.ignore()
            self.hide()

    def setup_tray_icon(self):
        trayIcon = QtWidgets.QSystemTrayIcon(QtGui.QIcon(":/images/icon.png"), self.main_window)
        menu = QtWidgets.QMenu()
        exitAction = menu.addAction("Exit")
        exitAction.triggered.connect(self.exit)
        trayIcon.setContextMenu(menu)
        trayIcon.setToolTip("Cliente FVA")
        trayIcon.activated.connect(self.toggle)
        trayIcon.show()

    def setup_current_tab_layout(self, new_layout):
        tab = self.usrSlots.currentWidget()
        QtWidgets.QWidget().setLayout(tab.layout())  # cleans current tab layout so a new one can be assigned
        tab.setLayout(new_layout)

    def setup_tab_default_layout(self):
        tab_default = TabDefault(QtWidgets.QWidget())
        self.setup_current_tab_layout(tab_default.tabDefaultLayout)

    def show(self):
        self.main_window.show()

    def hide(self):
        self.main_window.hide()

    def exit(self):
        self.close_window = True
        self.main_window.close()

    def toggle(self, reason):
        if reason == QtWidgets.QSystemTrayIcon.DoubleClick:
            if self.main_window.isVisible():
                self.hide()
            else:
                self.show()

    def open_my_requests(self, event):
        my_requests_ui = MyRequests(QtWidgets.QWidget())
        self.setup_current_tab_layout(my_requests_ui.myRequestsLayout)

    def open_my_signatures(self, event):
        my_signatures_ui = MySignatures(QtWidgets.QWidget())
        self.setup_current_tab_layout(my_signatures_ui.mySignaturesLayout)

    def open_settings(self, event):
        settings_ui = Settings(QtWidgets.QWidget())
        self.setup_current_tab_layout(settings_ui.settingsLayout)

    def open_request_signature(self, event):
        request_signature_ui = RequestSignature(QtWidgets.QWidget())
        self.setup_current_tab_layout(request_signature_ui.requestSignatureLayout)

    def open_request_authentication(self, event):
        request_authentication_ui = RequestAuthentication(QtWidgets.QWidget())
        self.setup_current_tab_layout(request_authentication_ui.requestAuthenticationLayout)

    def open_sign_validate(self, event):
        sign_validate_ui = SignValidate(QtWidgets.QWidget())
        self.setup_current_tab_layout(sign_validate_ui.signValidateLayout)

    def open_manage_contacts(self, event):
        manage_contacts_ui = ManageContacts(QtWidgets.QWidget())
        self.setup_current_tab_layout(manage_contacts_ui.manageContactsLayout)

    def open_manage_contact_groups(self, event):
        manage_contact_groups_ui = ManageContactGroups(QtWidgets.QWidget())
        self.setup_current_tab_layout(manage_contact_groups_ui.manageContactGroupsLayout)


def run():
    app = QtWidgets.QApplication(sys.argv)
    fva_client_ui = FVAClient(QtWidgets.QMainWindow())
    fva_client_ui.show()
    sys.exit(app.exec_())
