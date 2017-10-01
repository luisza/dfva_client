import time
from client_fva.monitor import Monitor


class OSDummyClient:
    def __init__(self):
        self.client = Monitor()
        self.client.start()
        self.client.signal.connect(self.request_pin_code)

    def request_pin_code(self, sender, **kw):
        
        obj = kw['obj']
        print(obj._type, obj.data)
        return obj
    
if __name__ == "__main__":
    client= OSDummyClient()
    time.sleep(55)
    client.client.close()