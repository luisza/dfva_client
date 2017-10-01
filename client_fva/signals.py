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


def get_signal_response(signal_response):
    for response in signal_response:
        if response[1] is not None:
            return response[1]


