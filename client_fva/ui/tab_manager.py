from PyQt5 import QtWidgets
from PyQt5.QtCore import QThreadPool, QObject
from client_fva.monitor import Monitor
from client_fva.ui.myrequests import MyRequests
from client_fva import signals
import logging
from client_fva.ui.fvadialog import FVASpeakerClient
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

logger = logging.getLogger('dfva_client')


class TabManager(QObject):

    def __init__(self, controller, main_app):
        super(TabManager, self).__init__()
        self.speakers = {}
        self.controller = controller
        self.main_app = main_app
        self.card_information = None
        self.card_count = 0

        self.threadpool = QThreadPool()
        logger.info("Multithreading with maximum %d threads" %
                    self.threadpool.maxThreadCount())
        self.monitor = Monitor()
        signals.connect('monitor_usb', self.token_information_event)

        self.threadpool.start(self.monitor)

    def token_information_event(self, sender, obj):
        if sender == 'monitor_usb':
            if obj._type == signals.USB_CONNECTED:
                self.create_tab(obj.data['person'], obj.data['slot'])
            elif obj._type == signals.USB_DISCONNECTED:
                self.remove_tab(obj.data['person'], obj.data['slot'])
            return obj

    def create_list_menu(self, fvaspeaker, name):
        if self.card_information is None:
            layout = self.controller.usrSlots.widget(0).layout()
            self.card_information = QTableWidget()
            self.card_information.setEditTriggers(
                QtWidgets.QAbstractItemView.NoEditTriggers)  # make it readonly
            # set row count
            self.card_information.setRowCount(0)
            # set column count
            self.card_information.setColumnCount(5)
            self.card_information.setHorizontalHeaderItem(
                0, QTableWidgetItem("Identificación"))
            self.card_information.setHorizontalHeaderItem(
                1, QTableWidgetItem("Nombre"))
            self.card_information.setHorizontalHeaderItem(
                2, QTableWidgetItem("Emisión"))
            self.card_information.setHorizontalHeaderItem(
                3, QTableWidgetItem("Vencimiento"))
            self.card_information.setHorizontalHeaderItem(
                4, QTableWidgetItem("Tipo"))
            layout.addWidget(self.card_information, 1, 0, 1, 2)
            #headers = self.card_information.horizontalHeader()
            # headers.setResizeMode(QtWidgets.QtHeaderView.ResizeToContents)

        certs = fvaspeaker.client.pkcs11client.get_certificate_info()
        if certs:
            cert = certs['authentication']
            self.card_information.insertRow(self.card_information.rowCount())
            self.card_information.setItem(
                self.card_count, 0, QTableWidgetItem(name))
            self.card_information.setItem(
                self.card_count, 1, QTableWidgetItem(cert['name']))
            self.card_information.setItem(self.card_count, 2, QTableWidgetItem(
                cert['cert_start'].strftime("%Y-%m-%d %H:%M")))
            self.card_information.setItem(self.card_count, 3, QTableWidgetItem(
                cert['cert_expire'].strftime("%Y-%m-%d %H:%M")))
            self.card_information.setItem(
                self.card_count, 4, QTableWidgetItem(cert['type']))
            self.card_count += 1
            self.card_information.resizeColumnsToContents()
        else:
            self.card_information.setRowCount(0)

    def create_tab(self, name, slot):
        print("create tab", name)
        my_requests_ui = MyRequests(QtWidgets.QWidget(), self.main_app)
        FVADialog = QtWidgets.QDialog()
        ui = FVASpeakerClient(FVADialog, slot, name)
        position = self.controller.usrSlots.count()
        self.speakers[name] = ui
        self.controller.usrSlots.insertTab(
            position, my_requests_ui.widget, name)
        self.controller.set_enabled_specific_menu_actions(True)
        self.create_list_menu(ui, name)

    def remove_tab(self, name, slot):
        index = -1
        for i in range(self.controller.usrSlots.count(), 0, -1):
            text = self.controller.usrSlots.tabText(i)
            if text == name:
                index = i
                break
        if index >= 0:
            self.controller.usrSlots.removeTab(index)
            self.speakers[name].closeEvent(None)
            self.speakers[name].client.close()
            del self.speakers[name]
        if self.controller.usrSlots.count() <= 1:
            self.controller.set_enabled_specific_menu_actions(False)

        if self.card_information is not None:
            pos_remove = -1
            for x in range(self.card_information.rowCount()):
                itemname = self.card_information.itemAt(x, 0)
                if name == itemname.text():
                    pos_remove = i
                    break
            if pos_remove != -1:
                self.card_information.removeRow(pos_remove)

    def close(self):
        self.monitor.close()
        for name in list(self.speakers.keys()):

            self.speakers[name].closeEvent(None)
            self.speakers[name].client.close()
            del self.speakers[name]
