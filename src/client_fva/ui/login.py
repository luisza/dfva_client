import datetime
import time

import requests
from PyQt5 import QtWidgets, QtCore

from client_fva.session_storage import SessionStorage


class EjecutionTimer(QtCore.QRunnable):
    def __init__(self, instance):
        self.instance = instance
        QtCore.QRunnable.__init__(self)
        self.threadpool = QtCore.QThreadPool()

    def run(self):
        start_time = datetime.datetime.now()
        while not self.instance.operation_finished:
            time.sleep(2)
            actual_time = datetime.datetime.now()
            difference = actual_time-start_time
            self.instance.on_timer(str(datetime.timedelta(seconds=difference.total_seconds())))


class PersonLoginOpers(QtCore.QThread):
    MAX_STEPS = 6

    def start_process_bar(self):
        self.progressbar = QtWidgets.QProgressBar(self.controller.centralWidget)
        self.progressbar.setFixedWidth(self.controller.centralWidget.width())

        self.progressbar.setStyleSheet("")
        self.progressbar.setProperty("value", 0)
        self.progressbar.setOrientation(QtCore.Qt.Horizontal)
        self.progressbar.setInvertedAppearance(False)
        self.progressbar.setTextDirection(QtWidgets.QProgressBar.BottomToTop)

        self.controller.statusBar.addWidget(self.progressbar)
        self.progressbar.setRange(0, self.MAX_STEPS)
        self.progressbar_status = 0
        self.progressbar.setValue(self.progressbar_status)
        self.operation_finished = False

    def end_process_bar(self):
        self.progressbar.setValue(self.MAX_STEPS)
        self.controller.statusBar.removeWidget(self.progressbar)
        self.operation_finished = True

    def __init__(self,serial, slot, controller):
        self.serial = serial
        self.slot = slot
        self.operation_finished = False

        self.controller = controller
        super(PersonLoginOpers, self).__init__()
        self.session_storage = SessionStorage.getInstance()
        self.threadpool = QtCore.QThreadPool()

    def run(self):
        self.start_process_bar()
        self.timer = EjecutionTimer(self)
        self.threadpool.start(self.timer)
        try:
            self.session_storage.session_info[self.serial]['personclient'].register(slot=self.slot)
        except requests.exceptions.ConnectionError:
            pass
        self.end_process_bar()

    def on_timer(self, minutes):
        self.progressbar_status = (self.progressbar_status + 1) % self.MAX_STEPS
        self.progressbar.setValue(self.progressbar_status)

        text = "Operación de autenticanción durante : "+minutes.split('.')[0]

        self.progressbar.setFormat(text)