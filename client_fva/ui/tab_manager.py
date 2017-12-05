from PyQt5 import  QtWidgets
from PyQt5.QtCore import QThreadPool, QObject
from client_fva.monitor import Monitor
from client_fva.ui.myrequests import MyRequests
from client_fva import signals

import logging
from client_fva.ui.fvadialog import  FVASpeakerClient
logger = logging.getLogger('dfva_client')

class TabManager(QObject):

    def __init__(self, controller, main_app):
        super(TabManager, self).__init__()
        self.speakers={}
        self.controller=controller
        self.main_app=main_app
        
        self.threadpool = QThreadPool()
        logger.info("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
        self.monitor = Monitor()
        self.monitor.signals.result.connect(self.token_information_event)
            
        self.threadpool.start(self.monitor)

    def token_information_event(self, sender, obj):
        if sender == 'monitor_usb':
            if obj._type == signals.USB_CONNECTED:
                self.create_tab(obj.data['person'], obj.data['slot'])
            elif obj._type == signals.USB_DISCONNECTED:
                self.remove_tab(obj.data['person'], obj.data['slot'])
            return obj

    def create_tab(self, name, slot):
        my_requests_ui = MyRequests(QtWidgets.QWidget(), self.main_app)
        FVADialog = QtWidgets.QDialog()
        ui = FVASpeakerClient(FVADialog, slot)
        position = self.controller.usrSlots.count()
        self.speakers[name]=ui
        self.controller.usrSlots.insertTab(position, my_requests_ui.widget, name)
        self.controller.set_enabled_specific_menu_actions(True)

    def remove_tab(self, name, slot):
        index=-1
        for i in range(self.controller.usrSlots.count(), 0, -1):
            text = self.controller.usrSlots.tabText(i)
            if text==name:
                index=i
                break
        if index>=0:
            self.controller.usrSlots.removeTab(index)
            self.speakers[name].closeEvent(None)
            del self.speakers[name]
        if self.controller.usrSlots.count() <= 1: 
            self.controller.set_enabled_specific_menu_actions(False)

    def close(self):
        self.monitor.close()

