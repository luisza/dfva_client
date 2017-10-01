import time
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
    
if __name__ == "__main__":
    client= OSDummyClient()
    time.sleep(55)
    client.client.close()