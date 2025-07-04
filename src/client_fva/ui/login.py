import datetime
import time

import requests
from PyQt5 import QtWidgets, QtCore
from client_fva import signals
from client_fva.session_storage import SessionStorage
from client_fva.user_settings import UserSettings


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
        self.progressbar_status = 0
        self.progressbar = self.controller.statusBarManager
        self.progressbar.show.emit()

    def end_process_bar(self):
        self.progressbar.hide.emit()
        self.operation_finished = True

    def __init__(self,serial, slot, controller):
        self.serial = serial
        self.slot = slot
        self.operation_finished = False

        self.controller = controller
        super(PersonLoginOpers, self).__init__()
        self.session_storage = SessionStorage.getInstance()
        self.threadpool = QtCore.QThreadPool()
        self.settings = UserSettings.getInstance()

    def run(self):
        self.start_process_bar()
        self.timer = EjecutionTimer(self)
        self.threadpool.start(self.timer)
        ok = False
        counttry = 0
        while not ok and counttry < self.settings.number_requests_before_fail:
            try:
                self.session_storage.session_info[self.serial]['personclient'].register(slot=self.slot)
                ok = True
            except requests.exceptions.ConnectionError:
                ok= False
                counttry += 1
        if not ok:
            signals.send('notify', signals.SignalObject(
                signals.NOTIFTY_ERROR,
                {'message': "Error en la red, no se puede autenticar al usuario, por favor verifique su conexión a internet"
             })
                             )
        self.end_process_bar()

    def on_timer(self, minutes):
        self.progressbar_status = (self.progressbar_status + 1) % self.MAX_STEPS
        self.progressbar.value.emit(self.progressbar_status)

        text = "Operación de autenticanción durante : "+minutes.split('.')[0]

        self.progressbar.text.emit(text)