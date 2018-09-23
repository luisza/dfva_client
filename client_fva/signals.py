'''

@author: luis
'''

import time
from PyQt5.QtCore import QMutex, QObject, pyqtSignal, QSharedMemory
from PyQt5.QtWidgets import QApplication
from uuid import uuid4
# Return response = {'pin': xxx, 'rejected': False}
PIN_REQUEST = 1
# Return response =  {'pin': xxx, 'code': xxx, 'rejected': False}
PIN_CODE_REQUEST = 2
USB_CONNECTED = 3
USB_DISCONNECTED = 4
NOTIFTY_ERROR = 5
NOTIFTY_INFO = 6


class SignalObject(object):
    '''
    Canales de comunicación

    - fva_client:

        * notify
        * monitor_usb
        * pin

    - identificacion:

        * fva_speaker

    El canal de identificación corresponde al número de identificación de la persona en cuestión.

    Datos enviados:

        * notify  {'message': 'XXX' }
        * monitor_usb  {'person': 'identificacion', 'slot': slot_obj }
        * pin {'serial': 'id slot'}
        * fva_speaker  {
              'a': HashAFirmarDocumento,
              'b': HashAFirmarResumen,
              "c": ResumenDelDocumento,
              "d": NombreDeLaEntidad,
              "e": LogoDeLaEntidad,
              "f": TimeoutEnSegundos,
              "g": IdDeLaSolicitud,
              "h": TipoDeFirma }

    .. note:: fva_speaker es lo que supongo que viene, por lo que recomiendo primero hacer un análisis de los datos

    Respuestas esperadas:

        * notify  {}
        * monitor_usb {}
        * pin  {'pin': 87888333 }
        * fva_speaker  {'pin': 99999, 'rejected': false, 'code': 'UY12345ZL'}

    '''
    _type = None
    data = None
    response = None

    def __init__(self, _type, data):
        self._type = _type
        self.data = data
        self.response = {}
        self.sid = uuid4().hex
        self.mutex = QMutex()

    def __repr__(self):
        return repr(self.sid) + " => "+repr(self.data)


class WorkerObject(QObject):
    result = pyqtSignal(str, SignalObject)


available_signals = {
    'notify': WorkerObject(),
    'monitor_usb': WorkerObject(),
    'pin': WorkerObject(),
    'fva_speaker': WorkerObject(),
}


def send(key, data):
    print("send: ", key)
    if key in available_signals:
        available_signals[key].result.emit(key, data)
        return data
    else:
        logger.error("Señal no disponible para enviar %r" % data)


def connect(key, func):
    print("connect: ", key)
    if key in available_signals:
        available_signals[key].result.connect(func)
    else:
        logger.error("Señal no disponible para conectar %r" % key)


objs = {}


def receive(obj, notify=False):
    if notify:
        objs[obj.sid] = obj
        obj.mutex.unlock()
        print(">>> ", repr(obj.response))
    else:
        obj.mutex.lock()
        print(objs)
        obj = objs[obj.sid]
        print("<<< ", repr(obj.response))
    return obj
