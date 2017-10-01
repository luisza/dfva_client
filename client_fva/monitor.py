'''
Created on 30 sep. 2017

@author: luisza
'''
from threading import Thread
from client_fva.pkcs11client import PKCS11Client
import time
import pkcs11
from blinker import signal
from client_fva import signals

daemon = True
class Monitor(PKCS11Client, Thread):
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

    def __init__(self, *args, **kwargs):

        self.settings = kwargs.get('settings', {})
        self.module_lib = self.get_module_lib()
        self.signal = signal('fva_client')
        Thread.__init__(self)

        
    def run(self):
        global daemon
        while daemon:
            self.detect_device()
            time.sleep(5)

            
    def detect_device(self, notify_exception=False):
        """
        """
        lib = pkcs11.lib(self.module_lib) 
        slots = lib.get_slots()
        tmp_device = []
        added_device = {}

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
                    added_device[serial]= data
                    self.send_add_signal(data)
            except pkcs11.exceptions.TokenNotRecognised as noToken:
                if notify_exception:
                    self.signal.send('notify', obj={
                        'message': "Un dispositivo ha sido encontrado, pero ninguna tarjeta pudo ser leída, por favor verifique que la tarjeta esté correctamente insertada"
                        })
            except Exception as e:
                if notify_exception:
                    self.signal.send('notify', obj={
    'message': "Ha ocurrido un error inesperado leyendo alguno de los dispositivos"
                        })

        self.connected_device.update(added_device)

        for connected_serial in tuple(self.connected_device.keys()):
            if connected_serial not in tmp_device:
                self.send_removed_signal(self.connected_device[connected_serial])
                self.connected_device.pop(connected_serial)
                
    def send_add_signal(self, data):
        sobj = signals.SignalObject(signals.USB_CONNECTED, data)
        self.signal.send('monitor_usb', obj=sobj)
        
    def send_removed_signal(self, data):
        sobj = signals.SignalObject(signals.USB_DISCONNECTED, data)
        self.signal.send('monitor_usb', obj=sobj)
        
    
    def close(self):
        global daemon 
        daemon = False
