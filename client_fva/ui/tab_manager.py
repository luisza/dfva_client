from PyQt5 import QtWidgets
from PyQt5.QtCore import QThreadPool, QObject

from client_fva.models.User import UserModel
from client_fva.monitor import Monitor
from client_fva.person import PersonClient
from client_fva.session_storage import SessionStorage
from client_fva.ui.myrequests import MyRequests
from client_fva import signals
import logging
from client_fva.ui.fvadialog import FVASpeakerClient
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

logger = logging.getLogger()


class TabManager(QObject):

    def __init__(self, controller, main_app):
        super(TabManager, self).__init__()
        self.speakers = {}
        self.controller = controller
        self.main_app = main_app
        self.card_information = None
        self.card_count = 0
        self.session_storage = SessionStorage.getInstance()
        self.threadpool = QThreadPool()
        logger.info("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
        self.monitor = Monitor()
        signals.connect('monitor_usb', self.token_information_event)

        self.threadpool.start(self.monitor)

    def token_information_event(self, sender, obj):
        if sender == 'monitor_usb':
            if obj._type == signals.USB_CONNECTED:
                self.create_tab(obj.data['person'], obj.data['slot'], obj.data['serial'])
            elif obj._type == signals.USB_DISCONNECTED:
                self.remove_tab(obj.data['person'], obj.data['slot'])
            return obj

    def create_list_menu(self, fvaspeaker, name, serial, slot):
        user = None
        if self.card_information is None:
            layout = self.controller.usrSlots.widget(0).layout()
            self.card_information = QTableWidget()
            self.card_information.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # make it readonly
            # set row count
            self.card_information.setRowCount(0)
            # set column count
            self.card_information.setColumnCount(7)
            self.card_information.setHorizontalHeaderItem(0, QTableWidgetItem("Identificación"))
            self.card_information.setHorizontalHeaderItem(1, QTableWidgetItem("Nombre"))
            self.card_information.setHorizontalHeaderItem(2, QTableWidgetItem("Emisión"))
            self.card_information.setHorizontalHeaderItem(3, QTableWidgetItem("Vencimiento"))
            self.card_information.setHorizontalHeaderItem(4, QTableWidgetItem("Tipo"))
            self.card_information.setHorizontalHeaderItem(5, QTableWidgetItem("Serial"))
            self.card_information.setHorizontalHeaderItem(6, QTableWidgetItem("Estado"))
            layout.addWidget(self.card_information, 1, 0, 1, 2)
            #headers = self.card_information.horizontalHeader()
            # headers.setResizeMode(QtWidgets.QtHeaderView.ResizeToContents)

        certs = fvaspeaker.client.pkcs11client.get_certificate_info(slot=slot)
        if certs:
            cert = certs['authentication']
            usercontrol = UserModel(db=self.session_storage.db)
            user = usercontrol.get_or_create_user(name,cert['first_name'], cert['last_name'])
            #index = len(self.session_storage.tabs)
            self.card_information.insertRow(self.card_information.rowCount())
            self.card_information.setItem(self.card_count, 0, QTableWidgetItem(name))
            self.card_information.setItem(self.card_count, 1, QTableWidgetItem(cert['name']))
            self.card_information.setItem(self.card_count, 2, QTableWidgetItem(
                cert['cert_start'].strftime("%Y-%m-%d %H:%M")))
            self.card_information.setItem(self.card_count, 3, QTableWidgetItem(
                cert['cert_expire'].strftime("%Y-%m-%d %H:%M")))
            self.card_information.setItem(self.card_count, 4, QTableWidgetItem(cert['type']))
            self.card_information.setItem(self.card_count, 5, QTableWidgetItem(serial))
            self.card_information.setItem(self.card_count, 6, fvaspeaker.status_widget)

            self.card_count += 1
            self.card_information.resizeColumnsToContents()
        else:
            self.card_information.setRowCount(0)
        return user

    def create_tab(self, name, slot, serial):
        my_requests_ui = MyRequests(QtWidgets.QWidget(), self.main_app)
        FVADialog = QtWidgets.QDialog()
        ui = FVASpeakerClient(FVADialog, slot, name)
        person = PersonClient(slot=slot, person=name, serial=serial)

        self.session_storage.tabs.append(slot)
        self.session_storage.serials.append(serial)
        self.session_storage.persons.append(person)
        position = len(self.session_storage.tabs)
        self.speakers[serial] = ui
        self.controller.usrSlots.insertTab(position, my_requests_ui.widget, "%s: %s"%(serial[-4:], name))
        self.controller.set_enabled_specific_menu_actions(True)
        user = self.create_list_menu(ui, name, serial, slot)
        self.session_storage.users.append(user)

    def remove_tab(self, name, slot):
        index = self.session_storage.tabs.index(slot)
        if index >=0:
            serial = self.session_storage.serials[index]
            self.controller.usrSlots.removeTab(index)
            self.speakers[serial].closeEvent(None)
            self.speakers[serial].close()
            del self.speakers[serial]
            self.card_information.removeRow(index-1)
            del self.session_storage.tabs[index]
            del self.session_storage.serials[index]
            del self.session_storage.persons[index]
            del self.session_storage.users[index]
            self.card_count -= 1

    def close(self):
        self.monitor.close()
        for name in list(self.speakers.keys()):
            self.speakers[name].closeEvent(None)
            self.speakers[name].close()
            del self.speakers[name]
