'''
Created on 17 ago. 2017

@author: luis
'''

import requests
import os
from client_fva.rsa import pem_to_base64
import json
import urllib
from base64 import b64decode, b64encode
from client_fva.pkcs11client import PKCS11Client
from pkcs11.mechanisms import Mechanism
from client_fva import signals
import logging
import time
from client_fva.user_settings import UserSettings
import pkcs11
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ca_bundle = os.path.join(BASE_DIR, 'certs/ca_bundle.pem')
from threading import Thread
from blinker import signal

logger = logging.getLogger('dfva_client')


class FVA_Base_client(PKCS11Client):
    info = None
    certificates = None
    session = None
    slot = None
    stop = False

    def __init__(self, *args, **kwargs):
        self.signal = kwargs.get('signal', signal('dfva_client'))
        kwargs['signal'] = self.signal
        self.settings = kwargs.get('settings', UserSettings())
        kwargs['settings'] = self.settings
        self.response = None
        PKCS11Client.__init__(self, *args, **kwargs)
        self.identification = self.get_identification()

    def start_the_negotiation(self):
        """
        Hace la negociación del protocolo de comunicación a utilizar
        """

        count = 0
        ok = False
        data = None
        while not ok and count < self.settings.number_requests_before_fail:
            try:
                data = self._request_start_negotiation()
            except requests.exceptions.ConnectionError:
                logger.warning(
                    "Error en requests iniciando negociación de la conexión, puede que no tenga acceso a internet")
            except Exception as e:
                logger.error(
                    "Error iniciando negociación de la conexión %r" % (e, ))
                # FiXME logging
            if data:
                ok = True
            count += 1

        return data

    def _request_start_negotiation(self):

        headers = {
            'User-Agent': self.settings.user_agent
        }

        # Fixme: poner en settings
        url = self.settings.bccr_fva_domain + self.settings.bccr_fva_url_negociation
        response = requests.get(url, verify=ca_bundle, headers=headers)
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

        count = 0
        ok = False
        response = None
        while not ok and count < self.settings.number_requests_before_fail:
            try:
                response = self._start_the_communication(data)
            except requests.exceptions.ConnectionError:
                logger.warning(
                    "Error en requests iniciando la comunicación")
            except Exception as e:
                logger.error("Error iniciando conexión %r" % (e, ))
                # FiXME logging
            if response is not None:
                ok = True
        return response

    def _start_the_communication(self, data):
        certificates = self.get_certificates()
        # url = self.base_url+'/connect'
        url = self.settings.bccr_fva_domain + \
            self.settings.bccr_fva_url_connect % (data['Url'])

        uname = os.uname()
        headers = {
            'Accept': 'text/event-stream',
            'CertificadoAutenticacion': pem_to_base64(certificates['authentication'].decode()),
            'CertificadoFirmante': pem_to_base64(certificates['sign'].decode()),
            'NombreDelSistemaOperativo': uname[0],
            'VersionDelSistemaOperativo': uname[3],
            'IpPrivada': '127.0.0.1',
            'Arquitectura': 'amd64' if uname[4] == 'x86_64' else 'x86',
            'NombreDelHost': uname[1],
            'User-Agent': self.settings.user_agent,
            'Content-Encoding': 'gzip'
        }

        self.response = requests.get(url, headers=headers,
                                     verify=ca_bundle,
                                     params=self.params,
                                     stream=True)
        return self.response

    def start_client(self):
        logger.info("Iniciando la comunicación con el BCCR de " +
                    self.identification)
        data = self.start_the_negotiation()
        response = None
        if data:
            response = self.start_the_communication(data)
        return response

    def process_messages(self, response):
        """
        Mientras existan mensajes por leer intenta procesar todo mensaje que venga del
        BCCR.
        """
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
                        self.signal.send('notify', obj={
                            'message': "Error al firmar, lo lamentamos por favor vuelva a intentarlo"
                        })

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
        sobj = signals.SignalObject(signals.PIN_CODE_REQUEST, data)
        respobj = signals.get_signal_response(
            self.signal.send('fva_speaker', obj=sobj))

        dev = {}
        dev["e"] = data['M'][0]['A'][0]['g']
        dev["d"] = 2 if respobj.response['rejected'] else 0
        dev["c"] = ""
        if not respobj.response['rejected']:
            dev["c"] = respobj.response['code']
            dev['b'], pin = self.get_signed_hash(data['M'][0]['A'][0]['b'],
                                                 pin=respobj.response['pin'],
                                                 data=data)
            dev['a'], pin = self.get_signed_hash(data['M'][0]['A'][0]['a'],
                                                 pin=pin,
                                                 data=data)

            if not all((dev['b'], dev['a'])):
                logger.error("Alguna firma incorrecta %r o %r" %
                             (dev['a'], dev['b']))
                dev["d"] = 2
            else:
                dev['b'] = dev['b'].decode()
                dev['a'] = dev['a'].decode()

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
                logger.error(
                    "Error enviando datos firmados %r" % (e, ))
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
            except pkcs11.exceptions.PinIncorrect:
                data['message'] = "Error PIN de %s incorrecto, por favor \
                vuelvalo a ingresar" % (self.identification,)
                sobj = signals.SignalObject(signals.PIN_REQUEST, data)
                respobj = signals.get_signal_response(
                    self.signal.send('fva_speaker', obj=sobj))
                pin = respobj.response['pin']
            except Exception as e:
                logger.error("Error get_signed_hash %r" % (e, ))

            if response:
                ok = True
            count += 1
        return response, pin

    def _get_signed_hash(self, _hash, pin):

        certificates = self.get_keys(pin=pin)
        d = certificates['sign']['priv_key'].sign(
            b64decode(_hash), mechanism=Mechanism.SHA256_RSA_PKCS)
        return b64encode(d)


class FVA_client(FVA_Base_client, Thread):
    def __init__(self, *args, **kwargs):

        FVA_Base_client.__init__(self, *args, **kwargs)
        Thread.__init__(self)
        self.internal_daemon = kwargs.get('daemon', True)

    def run(self):

        if self.identification is None:
            logger.error(
                "No se puede iniciar FVA_client, obtención de identificación no se realizó adecuadamente")
            return

        while self.internal_daemon:
            data = self.start_client()
            # start client could spend a lot of time connecting
            # and daemon could be close until client connect
            # so check again or threads can run forever
            if self.internal_daemon:
                if data is not None:
                    self.process_messages(data)
                else:
                    logger.info("Esperando para reconectar a " +
                                self.identification)
                    time.sleep(self.settings.reconnection_wait_time)
            elif data is not None and self.response is not None:
                self.response.connection.close()

    def close(self):
        self.internal_daemon = False
        if self.response:
            self.response.connection.close()
        logger.info("Terminando FVA_client de " + self.identification)


class OSDummyClient:
    def __init__(self):
        self.client = FVA_client()
        self.client.start()
        self.client.signal.connect(self.request_pin_code)

    def request_pin_code(self, sender, **kw):
        obj = kw['obj']
        print("%s dice:\n\n" % (obj.data['M'][0]['A'][0]['d'], ))
        print(obj.data['M'][0]['A'][0]['c'])

        obj.response['pin'] = input('Insert your pin: ')
        obj.response['code'] = input('Insert the code: ')
        obj.response['rejected'] = False
        return obj


"""
from client_fva.fva_speaker import FVA_client
c = FVA_client()
response = c.start()
c.process_messages(response)


from client_fva.fva_speaker import OSDummyClient
client= OSDummyClient()

"""
