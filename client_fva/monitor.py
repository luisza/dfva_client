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
    connected_device = {}
    module_lib = None

    def __init__(self, *args, **kwargs):

        self.settings = kwargs.get('settings', {})
        self.module_lib = self.get_module_lib()
        self.signal = signal('fva_client')
        Thread.__init__(self)

        
    def run(self):
        global daemon
        c=0
        while daemon:
            print("MOV ", c)
            self.detect_device()
            time.sleep(5)
            c+=1
            
    def detect_device(self):
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
                    added_device[serial]=slot
                    self.send_add_signal(slot)
            except Exception as e:
                import sys
                print(sys.exc_info()[0])
                

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
