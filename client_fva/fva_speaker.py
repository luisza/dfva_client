import json
import logging
import os

import pkcs11
import time
import urllib
from base64 import b64decode, b64encode
import requests
from PyQt5 import QtCore
from PyQt5.QtCore import QMutex
from pkcs11.mechanisms import Mechanism
from client_fva import signals
from client_fva.models.Pin import Secret
from client_fva.rsa import pem_to_base64
from client_fva.session_storage import SessionStorage
from client_fva.user_settings import UserSettings
import platform
from pathlib import Path

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ca_bundle = Path(BASE_DIR) / Path('certs/ca_bundle.pem')


logger = logging.getLogger()


class FVA_Base_client(object):
    stop = False
    pkcs11client = None

    def __init__(self, *args, **kwargs):
        self.settings = kwargs.get('settings', UserSettings.getInstance())
        self.slot_number = kwargs.pop('slot')
        self.pkcs11client = SessionStorage.getInstance().pkcs11_client
        self.response = None
        self.pin_response = None
        if self.pkcs11client is None:
            raise Exception("Pkcs11Client not found")
        self.identification = self.pkcs11client.get_identification(slot=self.slot_number)
        self.mutex = QMutex()

    def start_the_negotiation(self):
        """
        Hace la negociación del protocolo de comunicación a utilizar
        """
        data = None
        try:
            data = self._request_start_negotiation()
        except requests.exceptions.ConnectionError:
            logger.warning(
                "Error en requests iniciando negociación de la conexión, puede que no tenga acceso a internet")
        except Exception as e:
            logger.error("Error iniciando negociación de la conexión %r" % (e, ))
        return data

    def _request_start_negotiation(self):

        headers = {
            'User-Agent': self.settings.user_agent
        }
        url = self.settings.bccr_fva_domain + self.settings.bccr_fva_url_negotiation
        response = requests.get(url, verify=ca_bundle, headers=headers)
        if response.status_code != requests.codes.ok:
            logger.error("BCCR request_start_negotiation %s: %s" % (response.status_code, response.reason))
            raise Exception("Negociation unsuccessfull %s"%(response.reason,))
        result = response.json()
    # {'ProtocolVersion': '1.4',
    #  'DisconnectTimeout': 30.0,
    #  'ConnectionId': '80b6be12-b116-4180-a45f-1cb6acb3e2cc',
    #  'TryWebSockets': False,
    #  'ConnectionTimeout': 110.0,
    #  'LongPollDelay': 0.0,
    #  'ConnectionToken': 'w168cCG76CBH1LdnhhVgu4n9Gv/CRZn9AOqqxj7XQJE6PU4KV9I/jM10SSzqrZtwkXe0BhQLuJ4wZl0/89BOKU1PorJTkdcj/ObJivwg1pHAgmnT',
    #  'KeepAliveTimeout': 20.0,
    #  'TransportConnectTimeout': 5.0,
    #  'Url': '/wcfv2/Bccr.Firma.Fva.Hub/signalr'}
        # Fixme: poner en settings
        self.base_url = self.settings.bccr_fva_domain + result['Url']
        self.params = {
            'connectionData':   '[{"name":"administradordeclientes"}]',
            'connectionToken': result['ConnectionToken'],
            'connectionId': result['ConnectionId'],
            'transport': 'serverSentEvents',

        }
        return result

    def start_the_communication(self, data):
        """
        Inicia la comunicación con el servicio del BCCR
        """
        response = None
        try:
            response = self._start_the_communication(data)
        except requests.exceptions.ConnectionError:
            logger.warning("Error en requests iniciando la comunicación")
        except Exception as e:
            logger.error("Error iniciando conexión %r" % (e, ))

        if response is not None:
            if response.status_code != requests.codes.ok:
                logger.error("BCCR start_the_communication %s: %s"%(response.status_code, response.reason))
                response = None
        return response

    def _start_the_communication(self, data):
        certificates = self.pkcs11client.get_certificates(slot=self.slot_number)
        # url = self.base_url+'/connect'
        url = self.settings.bccr_fva_domain + \
            self.settings.bccr_fva_url_connect % (data['Url'])

        arch = platform.architecture()[0]
        headers = {
            'Accept': 'text/event-stream',
            'CertificadoAutenticacion': pem_to_base64(certificates['authentication'].decode()),
            'CertificadoFirmante': pem_to_base64(certificates['sign'].decode()),
            'NombreDelSistemaOperativo': platform.system(),
            'VersionDelSistemaOperativo': platform.release(),
            'IpPrivada': '127.0.0.1',
            'Arquitectura': 'amd64' if arch == '64bit' else 'x86',
            'NombreDelHost': platform.node(),
            'User-Agent': self.settings.user_agent,
            'Content-Encoding': 'gzip'
        }

        self.response = requests.get(url, headers=headers,
                                     verify=ca_bundle,
                                     params=self.params,
                                     stream=True)
        return self.response

    def start_client(self):
        logger.info("Iniciando la comunicación con el BCCR de " +  self.identification)
        data = self.start_the_negotiation()
        response = None
        if data:
            response = self.start_the_communication(data)
        if response is None or response.status_code != requests.codes.ok:
            return None
        return response

    def process_messages(self, response):
        """
        Mientras existan mensajes por leer intenta procesar todo mensaje que 
        venga del BCCR.
        """
        self.status_signal.emit(self.CONNECTED)
        for message in self.read_messages(response):
            try:
                data = json.loads(message)
            except:
                logger.info(message)
                continue
            if 'M' in data and data['M']:
                if "M" in data['M'][0] and data['M'][0]['M'] == "Firme":
                    signed = bool(self.sign(data))
                    if not signed:
                        signals.send('notify', signals.SignalObject(
                            signals.NOTIFTY_ERROR,
                            {'message':   "Error al firmar, lo lamentamos \
                            por favor vuelva a intentarlo"
                             })
                        )

    def read_messages(self, response):
        """
        Esto es parte de lo que viene
          @c(a="a")
          public String HashAFirmarDocumento;
          @c(a="b")
          public String HashAFirmarResumen;
          @c(a="c")
          public String ResumenDelDocumento;
          @c(a="d")
          public String NombreDeLaEntidad;
          @c(a="e")
          public String LogoDeLaEntidad;
          @c(a="f")
          public int TimeoutEnSegundos;
          @c(a="g")
          public int IdDeLaSolicitud;
          @c(a="h")
          public int TipoDeFirma;
        """

        for line in response.iter_lines():
            if not line:
                continue
            text = line.decode()
            if text and 'data: {}' != text:
                yield text.replace('data: ', '')

    def sign(self, data):
        params = {
            "H": "administradorDeClientes",
            "M": "FirmaRealizada",
            "A": [],
            "I": 0

        }

        self.password_request.emit(data)
        self.mutex.lock()
        self.mutex.lock()
        #sobj = signals.SignalObject(signals.PIN_CODE_REQUEST, data)
        #respobj = signals.receive(signals.send('fva_speaker', sobj))

        dev = {}
        dev["e"] = data['M'][0]['A'][0]['g']
        dev["d"] = 2 if self.pin_response['rejected'] else 0
        dev["c"] = ""
        if not self.pin_response['rejected']:
            dev["c"] = self.pin_response['code']
            dev['b'], pin = self.get_signed_hash(data['M'][0]['A'][0]['b'], pin=self.pin_response['pin'],
                                                 data=data)
            dev['a'], pin = self.get_signed_hash(data['M'][0]['A'][0]['a'], pin=pin, data=data)

            if not all((dev['b'], dev['a'])):
                logger.error("Alguna firma incorrecta %r o %r" %(dev['a'], dev['b']))
                dev["d"] = 2
            else:
                dev['b'] = dev['b'].decode()
                dev['a'] = dev['a'].decode()
        self.mutex.unlock()
        params['A'].append(dev)

        url = self.base_url + '/send'

        headers = {
            'User-Agent': self.settings.user_agent,
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        body = 'data=' + urllib.parse.quote_plus(json.dumps(params))
        return self.send_signed_data(url, body, headers)

    def send_signed_data(self, url, body, headers):
        """
        Notifica al BCCR que una firma se ha dado.
        Intenta tantas veces como **settings.number_requests_before_fail** indique en 
        caso de error.

        :params:

        url: ruta donde notificar
        body: mensaje a enviar ya procesado y en formato str
        headers: Encabezados http adicionales para enviar

        """
        count = 0
        ok = False
        data = None
        while not ok and count < self.settings.number_requests_before_fail:
            try:
                data = requests.post(
                    url, data=body,  verify=ca_bundle,
                    params=self.params, headers=headers)
            except requests.exceptions.ConnectionError:
                logger.warning(
                    "Error en requests enviando datos firmados, puede que no tenga acceso a internet")
            except Exception as e:
                logger.error("Error enviando datos firmados %r" % (e, ))
            if data:
                ok = True
            count += 1
            # FIXME: Mejorar el manejo de errores de HTTP que podría devolver
            # data = requests.post(
        self.sign_response = data
        return data

    def get_signed_hash(self, _hash, pin=None, data=None):
        """
        Firma el **_hash** suministrado con el **pin** suminstrado por el usuario y utiliza
        **data** por si el pin es incorrecto.

        Devuelve el hash firmado en base64 como string.
        """
        count = 0
        ok = False
        response = None
        while not ok and count < self.settings.max_pin_fails:
            try:
                response = self._get_signed_hash(_hash, pin)

            except pkcs11.exceptions.PinIncorrect as e:
                data['message'] = "Error PIN de %s incorrecto, por favor vuelvalo a ingresar" % (self.identification,)
                self.password_request.emit(data)
                self.mutex.lock()
                #self.mutex.lock()
                pin = self.pin_response['pin']

            except Exception as e:
                logger.error("Error get_signed_hash %r" % (e, ))

            if response:
                ok = True
            count += 1
        return response, pin

    def _get_signed_hash(self, _hash, pin):
        pin = Secret(pin, decode=True)
        certificates = self.pkcs11client.get_keys(pin=pin, slot=self.slot_number)
        d = certificates['sign']['priv_key'].sign(b64decode(_hash), mechanism=Mechanism.SHA256_RSA_PKCS)
        return b64encode(d)

    def set_pin_response(self, response):
        self.pin_response = response
        self.mutex.unlock()

class FVA_client(FVA_Base_client, QtCore.QThread):
    status_signal = QtCore.pyqtSignal(int)
    password_request = QtCore.pyqtSignal(dict)

    CONNECTING = 0
    CONNECTED = 1
    ERROR = 2

    def __init__(self, *args, **kwargs):
        FVA_Base_client.__init__(self, *args, **kwargs)
        QtCore.QThread.__init__(self, None)
        self.internal_daemon = kwargs.get('daemon', True)
        #self.serial = kwargs.get('serial', None)  # serial must be set

        self.connection_tries = 0
        self.daemon_active = False

    def run(self):
        if self.identification is None:
            logger.error("No se puede iniciar FVA_client, obtención de identificación no se realizó adecuadamente")
            return
        self.daemon_active = True
        self.status_signal.emit(self.CONNECTING)

        while self.internal_daemon and self.connection_tries != self.settings.number_requests_before_fail:
            data = self.start_client()
            # start client could spend a lot of time connecting
            # and daemon could be close until client connect
            # so check again or threads can run forever
            if self.internal_daemon:
                if data is not None:
                    self.process_messages(data)
                    self.connection_tries = 0
                else:
                    logger.info("Esperando para reconectar a " + self.identification)
                    self.connection_tries += 1
                    time.sleep(self.settings.reconnection_wait_time)
        if self.connection_tries == self.settings.number_requests_before_fail:
            logger.error("Max number of retries, closing connection")
        if self.response is not None:
            self.status_signal.emit(self.ERROR)
            self.response.connection.close()
            self.response = None
            self.daemon_active = False

    def close(self):
        self.internal_daemon = False
        self.daemon_active = False
        if self.response:
            self.response.connection.close()
            self.response = None
        logger.info("Terminando FVA_client de " + self.identification)



class OSDummyClient:
    def __init__(self):
        self.client = FVA_client()
        self.client.start()
        signals.connect('pin', self.request_pin_code)

    def request_pin_code(self, sender, **kw):
        obj = kw['obj']
        print("%s dice:\n\n" % (obj.data['M'][0]['A'][0]['d'], ))
        print(obj.data['M'][0]['A'][0]['c'])

        obj.response['pin'] = input('Insert your pin: ')
        obj.response['code'] = input('Insert the code: ')
        obj.response['rejected'] = False
        signals.receive(obj, notify=True)


"""
from client_fva.fva_speaker import FVA_client
c = FVA_client()
response = c.start()
c.process_messages(response)


from client_fva.fva_speaker import OSDummyClient
client= OSDummyClient()

"""
