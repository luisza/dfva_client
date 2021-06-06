import os
from pathlib import Path

from PyQt5.QtCore import QThread
import logging
import time
from client_fva.user_settings import UserSettings
from client_fva.pkcs11client import PKCS11Client, SlotNotFound
from client_fva import signals
from PyQt5.QtCore import  pyqtSignal
logger = logging.getLogger()


class Monitor(QThread):
    connected_device = {}
    add_card = pyqtSignal(int, str, str)
    rm_card = pyqtSignal(int, str, str)

    def __init__(self, *args, **kwargs):
        self.session_storage = kwargs['session_storage']

        self.settings = kwargs.get('settings', UserSettings.getInstance())
        self.devices = {}
        kwargs['settings'] = self.settings
        kwargs['cached'] = False
        self.pkcs11client = PKCS11Client(*args, **kwargs)
        self.session_storage.pkcs11_client = self.pkcs11client
        super().__init__()
        self.enabled = True



    def detect_device(self, notify_exception=False):
        """
        Identifica cambios en las tarjetas conectadas, es utilizado
        normalmente de forma automática con el monitor, pero se puede llamar
        usando detect_device( notify_exception=True) para que envíe notificaciones
        de los errores presentados al detectar las tarjetas.
        """


        logger.debug("Installation path: "+str(self.settings.get_installation_path()))
        logger.debug("Monitor: detect device")
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
            logger.error("%r" % (noToken,))
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

    def run(self):
        logger.info("Iniciando monitor")
        while self.enabled:
            self.detect_device()
            time.sleep(10)

    def send_add_signal(self, data):
        #sobj = signals.SignalObject(signals.USB_CONNECTED, data)
        logger.info("Tarjeta conectada %s" % (data['person'],))
        #self.tab_manager.add_card( data['person'], data['slot'], data['serial'])
        #signals.send('monitor_usb', sobj)
        self.add_card.emit(int(data['slot']), data['person'], data['serial'])

    def send_removed_signal(self, data):
        #sobj = signals.SignalObject(signals.USB_DISCONNECTED, data)
        logger.info("Tarjeta desconectada %s" % (data['person'],))
        #self.tab_manager.remove_card(data['person'], data['slot'], data['serial'])
        #signals.send('monitor_usb', sobj)
        self.rm_card.emit(int(data['slot']), data['person'], data['serial'])

    def close(self):
        self.enabled = False
