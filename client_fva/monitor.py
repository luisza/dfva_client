'''
Created on 30 sep. 2017

@author: luisza
'''
from PyQt5.QtCore import QRunnable, pyqtSlot, pyqtSignal, QObject, QMutex
from client_fva.pkcs11client import PKCS11Client
import time
import pkcs11
#from blinker import signal
from client_fva import signals
import logging
logger = logging.getLogger('dfva_client')

from smartcard.CardMonitoring import CardMonitor, CardObserver


class DfvaCardObserver(CardObserver):
    def __init__(self, *args, **kwargs):
        self.eventmanager = kwargs.pop('eventmanager')
        super(DfvaCardObserver, self).__init__(*args, **kwargs)

    def update(self, observable, actions):
        (addedcards, removedcards) = actions
        self.eventmanager.detect_device()


class WorkerObject(QObject):
    result = pyqtSignal(str, signals.SignalObject)


class Monitor(PKCS11Client, QRunnable):
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
    module_lib = None
    lib = None

    def __init__(self, *args, **kwargs):

        self.settings = kwargs.get('settings', {})
        self.module_lib = self.get_module_lib()
        #self.signal = kwargs.get('signal', signal('fva_client'))
        QRunnable.__init__(self)
        self.signals = WorkerObject()
        self.setAutoDelete(True)
        self.cardmonitor = None
        self.cardobserver = None
        self.mutex = QMutex()

    @pyqtSlot()
    def run(self):
        logger.info("Iniciando monitor")
        self.cardmonitor = CardMonitor()
        self.cardobserver = DfvaCardObserver(eventmanager=self)
        self.cardmonitor.addObserver(self.cardobserver)
        while True:
            time.sleep(3000)

    def get_slots(self):
        slots = []
        if self.lib is None:
            try:
                self.lib = pkcs11.lib(self.module_lib)
            except Exception as e:
                self.signal.send('notify', obj={
                    'message': "La biblioteca instalada no funciona para leer las tarjetas, esto puede ser porque no ha instalado las bibliotecas necesarias o porque el sistema operativo no está soportado"
                })
                logger.error("Error abriendo dispositivos PKCS11 %r" % (e,))
        if self.lib:
            slots = self.lib.get_slots()
        return slots

    def detect_device(self, notify_exception=False):
        """
        Identifica cambios en las tarjetas conectadas, es utilizado 
        normalmente de forma automática con el monitor, pero se puede llamar 
        usando detect_device( notify_exception=True) para que envíe notificaciones 
        de los errores presentados al detectar las tarjetas.
        """
        self.mutex.lock()
        tmp_device = []
        added_device = {}
        slots = self.get_slots()
        for slot in slots:
            try:
                serial = slot.get_token().serial.decode("utf-8")
                if serial in self.connected_device:
                    tmp_device.append(serial)
                else:
                    tmp_device.append(serial)
                    self.slot = slot
                    person = self.get_identification()
                    data = {'slot': slot,
                            'person': person}
                    added_device[serial] = data
                    self.send_add_signal(data)
            except pkcs11.exceptions.TokenNotRecognised as noToken:
                if notify_exception:
                    self.signals.result.emit('notify', {
                        'message': "Un dispositivo ha sido encontrado, pero ninguna tarjeta pudo ser leída, por favor verifique que la tarjeta esté correctamente insertada"
                    })
            except Exception as e:
                if notify_exception:
                    self.signals.result.emit('notify',  {
                        'message': "Ha ocurrido un error inesperado leyendo alguno de los dispositivos"
                    })

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
        self.signals.result.emit('monitor_usb', sobj)

    def send_removed_signal(self, data):
        sobj = signals.SignalObject(signals.USB_DISCONNECTED, data)
        logger.info("Tarjeta desconectada %s" % (data['person'],))
        self.signals.result.emit('monitor_usb', sobj)

    def close(self):
        logger.info("Terminando monitor")
        if self.cardmonitor and self.cardmonitor.countObservers() <= 0:
            self.cardmonitor.rmthread.stopEvent.set()
            self.cardmonitor = None
        if self.cardmonitor and self.cardobserver:
            self.cardmonitor.deleteObserver(self.cardobserver)
            self.cardobserver = None
