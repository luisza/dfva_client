'''
Created on 30 sep. 2017

@author: luisza
'''

import logging
import time

from PyQt5.QtCore import QMutex, QObject, QRunnable, pyqtSignal, pyqtSlot
from blinker import signal
from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.ReaderMonitoring import ReaderMonitor, ReaderObserver

from client_fva import signals


from client_fva.pkcs11client import PKCS11Client, SlotNotFound
from client_fva.session_storage import SessionStorage
from client_fva.user_settings import UserSettings

logger = logging.getLogger()


class DFVAReaderObserver(ReaderObserver):
    def __init__(self, *args, **kwargs):
        self.eventmanager = kwargs.pop('eventmanager')
        super(DFVAReaderObserver, self).__init__(*args, **kwargs)

    def update(self, observable, actions):
        (addedreaders, removedreaders) = actions
        logger.debug("Added readers %r" % addedreaders)
        logger.debug("Removed readers %r" % removedreaders)
        self.eventmanager.detect_device()


class DfvaCardObserver(CardObserver):
    def __init__(self, *args, **kwargs):
        self.eventmanager = kwargs.pop('eventmanager')
        super(DfvaCardObserver, self).__init__(*args, **kwargs)

    def update(self, observable, actions):
        (addedcards, removedcards) = actions
        self.eventmanager.detect_device()

pkcs11=PKCS11Client()

class WorkerObject(QObject):
    result = pyqtSignal(str, signals.SignalObject)


class Monitor(QRunnable):
    """
    Monitoriza los dispositivos pkcs11 conectados a la computadora.
    Lanza 2 eventos:

    * Dispositivo conectado (signals.USB_CONNECTED)
    * Dispositivo desconectado (signals.USB_DISCONNECTED)

    Este módulo utiliza blinker para emitir las señales. Un ejemplo de uso puede ser:

    .. code:: python 

        from client_fva.monitor import Monitor
        from client_fva import signals
        class OSDummyClient:
            def __init__(self):
                self.client = Monitor()
                self.client.start()
                self.client.signal.connect(self.token_information_event)

            def token_information_event(self, sender, **kw):

                obj = kw['obj']
                if obj._type == signals.USB_CONNECTED:
                    print("Conectando ", obj._type)
                elif obj._type == signals.USB_DISCONNECTED:
                    print("Desconectando ", obj._type)
                print(obj.data)
                return obj

    No se requiere devolver nada, pero es bueno para seguir con el formato, de otras señales
    """
    connected_device = {}
    lib = None

    def __init__(self, *args, **kwargs):
        self.settings = kwargs.get('settings', UserSettings.getInstance())
        kwargs['settings'] = self.settings
        kwargs['cached'] = False
        self.session_storage = SessionStorage.getInstance()
        self.pkcs11client = PKCS11Client(*args, **kwargs)
        self.settings = kwargs.get('settings', {})
        self.module_lib = self.pkcs11client.get_module_lib()
        self.signal = kwargs.get('signal', signal('fva_client'))
        self.session_storage.pkcs11_client = self.pkcs11client
        QRunnable.__init__(self)

        self.setAutoDelete(True)
        self.cardmonitor = None
        self.cardobserver = None
        self.mutex = QMutex()

    @pyqtSlot()
    def run(self):
        logger.info("Iniciando monitor")
        self.readermonitor = ReaderMonitor()
        self.cardmonitor = CardMonitor()
        self.cardobserver = DfvaCardObserver(eventmanager=self)
        self.readerobserver = DFVAReaderObserver(eventmanager=self)
        self.cardmonitor.addObserver(self.cardobserver)
        self.readermonitor.addObserver(self.readerobserver)

        while True:
            time.sleep(self.settings.wait_for_scan_new_device)

    def detect_device(self, notify_exception=False):
        """
        Identifica cambios en las tarjetas conectadas, es utilizado 
        normalmente de forma automática con el monitor, pero se puede llamar 
        usando detect_device( notify_exception=True) para que envíe notificaciones 
        de los errores presentados al detectar las tarjetas.
        """
        logger.debug("Monitor: detect device")
        self.mutex.lock()
        tmp_device = []
        added_device = {}
        try:
            for tokeninfo in self.pkcs11client.get_tokens_information():
                slot = tokeninfo['slot']
                serial = tokeninfo['serial']
                if serial in self.connected_device:
                    tmp_device.append(serial)
                else:
                    tmp_device.append(serial)
                    person = self.pkcs11client.get_identification(slot=slot)
                    data = {'slot': slot, 'person': person, 'serial': serial}
                    added_device[serial] = data
                    self.send_add_signal(data)
        except SlotNotFound as notoken:
            pass
        except Exception as noToken:
            if notify_exception:
                signals.send('notify', {'message': "Un dispositivo ha sido encontrado, pero ninguna tarjeta pudo ser "
                                                   "leída, por favor verifique que la tarjeta esté correctamente "
                                                   "insertada"})
            logger.error("%r"%(noToken,))
            # except Exception as e:
            #     if notify_exception:
            #         signals.result.emit('notify',  {
            #             'message': "Ha ocurrido un error inesperado leyendo alguno de los dispositivos"
            #         })


        self.connected_device.update(added_device)

        for connected_serial in tuple(self.connected_device.keys()):
            if connected_serial not in tmp_device:
                self.send_removed_signal(
                    self.connected_device[connected_serial])
                self.connected_device.pop(connected_serial)
        self.mutex.unlock()

    def send_add_signal(self, data):
        sobj = signals.SignalObject(signals.USB_CONNECTED, data)
        logger.info("Tarjeta conectada %s" % (data['person'],))
        signals.send('monitor_usb', sobj)

    def send_removed_signal(self, data):
        sobj = signals.SignalObject(signals.USB_DISCONNECTED, data)
        logger.info("Tarjeta desconectada %s" % (data['person'],))
        signals.send('monitor_usb', sobj)

    def close(self):
        logger.info("Terminando monitor")
        if self.cardmonitor and self.cardmonitor.countObservers() <= 0:
            self.cardmonitor.rmthread.stopEvent.set()
            self.cardmonitor = None
        if self.cardmonitor and self.cardobserver:
            self.cardmonitor.deleteObserver(self.cardobserver)
            self.cardobserver = None
