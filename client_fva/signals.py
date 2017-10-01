'''

@author: luis
'''

# Return response = {'pin': xxx, 'rejected': False}
PIN_REQUEST = 1
# Return response =  {'pin': xxx, 'code': xxx, 'rejected': False}
PIN_CODE_REQUEST = 2
USB_CONNECTED = 3 
USB_DISCONNECTED = 4


class SignalObject(object):
    '''
    Canales de comunicación
    
    - fva_client: 
        * notify
        * monitor_usb
    
    - identificacion: 
        * fva_speaker
        
    El canal de identificación corresponde al número de identificación de la persona en cuestión.
    '''
    _type = None
    data = None
    response = None

    def __init__(self, _type, data):
        self._type = _type
        self.data = data
        self.response = {}


def get_signal_response(signal_response):
    for response in signal_response:
        if response[1] is not None:
            return response[1]


