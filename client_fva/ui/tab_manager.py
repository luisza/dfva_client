from PyQt5 import QtWidgets
from PyQt5.QtCore import QThreadPool, QObject

from client_fva.models.User import UserModel
from client_fva.monitor import Monitor
from client_fva.person import PersonClient
from client_fva.session_storage import SessionStorage
from client_fva.ui.signvalidate import SignValidate
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
        self.monitor = Monitor(session_storage=self.session_storage)
        self.monitor.start()
        self.monitor.add_card.connect(self.add_card)
        self.monitor.rm_card.connect(self.rm_card)


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
            self.card_information.setHorizontalHeaderItem(0, QTableWidgetItem("Alias"))
            self.card_information.setHorizontalHeaderItem(1, QTableWidgetItem("Identificación"))
            self.card_information.setHorizontalHeaderItem(2, QTableWidgetItem("Nombre"))
            self.card_information.setHorizontalHeaderItem(3, QTableWidgetItem("Emisión"))
            self.card_information.setHorizontalHeaderItem(4, QTableWidgetItem("Vencimiento"))
            self.card_information.setHorizontalHeaderItem(5, QTableWidgetItem("Tipo"))
            self.card_information.setHorizontalHeaderItem(6, QTableWidgetItem("Serial"))
            self.card_information.setHorizontalHeaderItem(7, QTableWidgetItem("Estado"))
            self.card_information.setColumnHidden(0, True)
            layout.addWidget(self.card_information, 1, 0, 1, 2)
            self.card_information.contextMenuEvent = self.edit_serial_menu_event

        certs = fvaspeaker.client.pkcs11client.get_certificate_info(slot=slot)
        if certs:
            cert = certs['authentication']
            usercontrol = UserModel(db=self.session_storage.db)
            user = usercontrol.get_or_create_user(name,cert['first_name'], cert['last_name'])
            #index = len(self.session_storage.tabs)
            self.card_information.insertRow(self.card_information.rowCount())
            self.card_information.setItem(self.card_count, 0, QTableWidgetItem(serial))
            self.card_information.setItem(self.card_count, 1, QTableWidgetItem(name))
            self.card_information.setItem(self.card_count, 2, QTableWidgetItem(cert['name']))
            self.card_information.setItem(self.card_count, 3, QTableWidgetItem(
                cert['cert_start'].strftime("%Y-%m-%d %H:%M")))
            self.card_information.setItem(self.card_count, 4, QTableWidgetItem(
                cert['cert_expire'].strftime("%Y-%m-%d %H:%M")))
            self.card_information.setItem(self.card_count, 5, QTableWidgetItem(cert['type']))
            self.card_information.setItem(self.card_count, 6, QTableWidgetItem(serial))
            self.card_information.setItem(self.card_count, 7, fvaspeaker.status_widget)

            self.card_count += 1
            self.card_information.resizeColumnsToContents()
        else:
            self.card_information.setRowCount(0)
        return user

    def add_card(self, slot, name,  serial):
        self.session_storage.session_info[serial] = {
            'tabnumber': 0,
            'slot': slot,
            'identification':  name,
            'session_key': None,
            'user': None,
            'personclient': None,
            'fvaspeaker': None,
            'alias': "%s: %s" % (serial[-4:], name)
        }
        self.create_tab(name, slot, serial)

    def rm_card(self, slot, name,  serial):
        self.remove_tab(serial)
        del self.session_storage.session_info[serial]

    def create_tab(self, name, slot, serial):
        FVADialog = QtWidgets.QDialog()
        self.session_storage.session_info[serial]['tabnumber'] = self.controller.usrSlots.count()
        self.session_storage.session_info[serial]['personclient'] = PersonClient(slot=slot, person=name, serial=serial)
        self.session_storage.session_info[serial]['fvaspeaker'] = FVASpeakerClient(FVADialog, slot, name)

        sign_validate_ui = SignValidate(QtWidgets.QWidget(), self.main_app, serial)
        self.session_storage.last_layout = sign_validate_ui
        alias = self.session_storage.alias.filter(serial)
        self.session_storage.session_info[serial]['alias'] = alias[0] if alias else self.session_storage.session_info[serial]['alias']

        self.controller.usrSlots.insertTab(self.controller.usrSlots.count(), sign_validate_ui.widget,
                                           self.session_storage.session_info[serial]['alias'])
        self.controller.set_enabled_specific_menu_actions(True)
        user = self.create_list_menu(self.session_storage.session_info[serial]['fvaspeaker'], name, serial, slot)
        self.session_storage.session_info[serial]['user'] = user
        self.session_storage.session_info[serial]['personclient'].register(slot=slot)

    def re_index_tabnumber(self):
        for x in range(0, self.controller.usrSlots.count()):
            text = self.controller.usrSlots.tabText(x)
            for serial in self.session_storage.session_info:
                if self.session_storage.session_info[serial]['alias'] == text:
                    self.session_storage.session_info[serial]['tabnumber'] = x

    def remove_tab(self, serial):
        index = self.session_storage.session_info[serial]['tabnumber']
        if index >=0:
            self.controller.usrSlots.removeTab(index)
            self.session_storage.session_info[serial]['fvaspeaker'].closeEvent(None)
            self.session_storage.session_info[serial]['fvaspeaker'].close()
            del self.session_storage.session_info[serial]['fvaspeaker']
            self.card_information.removeRow(index)
            self.card_count -= 1
            self.re_index_tabnumber()

    def close(self):
        self.monitor.close()
        for serial in self.session_storage.session_info:
            self.remove_tab(serial)

    def edit_serial_menu_event(self, pos):
        if self.card_information.selectedIndexes():
            selected = self.card_information.currentIndex()  # user can only select one contact at the time
            if selected.isValid():
                row, column = selected.row(), selected.column()
                menu = QtWidgets.QMenu()
                menu.setStyleSheet("QMenu::item{color:rgb(76, 118, 82);background-color:rgb(216, 230, 225);}")
                edit_action = menu.addAction("Asignar Alias")
                action = menu.exec_(self.card_information.mapToGlobal(pos.pos()))
                if action == edit_action:
                    self.edit_serial(row, column)

    def re_alias(self):
        pass

    def edit_serial(self, row, column):
        alias_name, done1 = QtWidgets.QInputDialog.getText(self.session_storage.parent_widget,
                                                           'Ingrese un alias para esta tarjeta', 'Alias:')
        if done1:
            serial = self.card_information.item(row, 0).text()
            alias = self.session_storage.alias.create_update(serial, alias_name)
            self.session_storage.session_info[serial]['alias'] = alias
            self.re_alias()