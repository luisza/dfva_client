'''
Created on 17 ago. 2017

@author: luis
'''

import requests
import os
import OpenSSL
from pkcs11 import Mechanism
from pkcs11.constants import Attribute
from pkcs11.constants import ObjectClass
import pkcs11
from client_fva.rsa import pem_to_base64
import json
import urllib
from base64 import b64decode, b64encode
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ca_bundle = os.path.join(BASE_DIR, 'lib/certs/ca_bundle.pem')


class FVA_client:
    info = None
    certificates = None
    session = None
    slot = None
    stop = False

    def __init__(self):
        self.slot = self.get_slot()

    def start_the_negotiation(self):
        headers = {
            'User-Agent': 'SignalR (lang=Java; os=linux; version=2.0)'
        }

        url = "https://www.firmadigital.go.cr/wcfv2/Bccr.Firma.Fva.Hub/signalr/negotiate?clientProtocol=1.4&connectionData=%5B%7B%22name%22%3A%22administradordeclientes%22%7D%5D"
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
        self.base_url = 'https://www.firmadigital.go.cr' + result['Url']
        self.params = {
            'connectionData':   '[{"name":"administradordeclientes"}]',
            'connectionToken': result['ConnectionToken'],
            'connectionId': result['ConnectionId'],
            'transport': 'serverSentEvents',

        }
        return result

    def start_the_communication(self, data):
        certificates = self.get_certificates()
        # url = self.base_url+'/connect'
        url = """https://www.firmadigital.go.cr/%s/connect""" % (data['Url'])

        uname = os.uname()
        headers = {
            'Accept': 'text/event-stream',
            'CertificadoAutenticacion': pem_to_base64(certificates['authentication']['pem'].decode()),
            'CertificadoFirmante': pem_to_base64(certificates['sign']['pem'].decode()),
            'NombreDelSistemaOperativo': uname[0],
            'VersionDelSistemaOperativo': uname[3],
            'IpPrivada': '127.0.0.1',
            'Arquitectura': 'amd64' if uname[4] == 'x86_64' else 'x86',
            'NombreDelHost': uname[1],
            'User-Agent': 'SignalR (lang=Java; os=linux; version=2.0)',
            'Content-Encoding': 'gzip'
        }

        self.response = requests.get(url, headers=headers,
                                     verify=ca_bundle,
                                     params=self.params,
                                     stream=True)

        return self.response

    def get_slot(self):
        """Obtiene el primer slot (tarjeta) disponible
        .. warning:: Solo usar en pruebas y mejorar la forma como se capta
        """
        lib = pkcs11.lib(self.get_module_lib())
        slots = lib.get_slots()
        if not slots:
            raise Exception("PKCS11: Slot not found")
        self.slot = slots[0]
        return self.slot

    def get_module_lib(self):
        """Obtiene la biblioteca de comunicación con la tarjeta """
        if 'PKCS11_MODULE' in os.environ:
            return os.environ['PKCS11_MODULE']

        if os.path.exists('/usr/lib/libASEP11.so'):
            return '/usr/lib/libASEP11.so'

        try:
            import platform
            arch = platform.architecture()[0]
            if arch == '64bit':
                arch = 'x86_64'
            else:
                arch = 'x86'

            BASE_DIR = os.path.dirname(
                os.path.dirname(os.path.abspath(__file__)))
            path = os.path.join(
                BASE_DIR, 'clients/lib/%s/libASEP11.so' % (arch, ))
            if os.path.exists(path):
                return path
        except Exception as e:
            raise Exception(
                "Sorry not PKCS11 module found, please use export PKCS11_MODULE='<path>' before call python ")

    def get_pin(self):
        """Obtiene el pin de la tarjeta para iniciar sessión"""
        if 'PKCS11_PIN' in os.environ:
            return os.environ['PKCS11_PIN']
        else:
            return input("Write your pin: ")

        raise Exception(
            'Sorry PIN is Needed, we will remove this, but for now use export PKCS11_PIN=<pin> before call python')

    def get_session(self):
        """Obtiene o inicializa una sessión para el uso de la tarjeta.
        .. warning:: Ojo cachear la session y revisar si está activa
        """
        # Fixme: Verificar si la sessión está activa y si no lo está entonces
        # volver a iniciarla
        if self.session is None:
            self.token = self.slot.get_token()
            self.session = self.token.open(user_pin=self.get_pin())
            return self.session
        return self.session

    def get_certificates(self):
        """Extrae los certificados dentro del dispositivo y los guarda de forma estructurada para simplificar el acceso"""
        if self.certificates is None:
            certs = {}
            cert_label = []
            session = self.get_session()
            for cert in session.get_objects({
                    Attribute.CLASS: ObjectClass.CERTIFICATE}):
                x509 = OpenSSL.crypto.load_certificate(
                    OpenSSL.crypto.FILETYPE_ASN1, cert[Attribute.VALUE])
                certs[cert[3]] = {
                    'cert': cert,
                    'pub_key': OpenSSL.crypto.dump_publickey(OpenSSL.crypto.FILETYPE_PEM, x509.get_pubkey()),
                    'pem': OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, x509),
                }
                cert_label.append(cert[3])

            for privkey in session.get_objects({Attribute.CLASS: ObjectClass.PRIVATE_KEY}):
                if privkey.label in certs:
                    certs[privkey.label]['priv_key'] = privkey

            self.certificates = {
                'authentication': certs[cert_label[0]],
                'sign': certs[cert_label[1]]
            }
        return self.certificates

    def start(self):
        data = self.start_the_negotiation()
        response = self.start_the_communication(data)
        return response

    def process_messages(self, response):
        for message in self.read_messages(response):
            try:
                data = json.loads(message)
            except:
                print(message)
                continue
            if 'M' in data and data['M']:
                if "M" in data['M'][0] and data['M'][0]['M'] == "Firme":
                    self.sign(data)

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
        dev = {}
        dev["e"] = data['M'][0]['A'][0]['g']
        dev["d"] = 0
        dev["c"] = input('Código: ')
        dev['b'] = self.get_signed_hash(data['M'][0]['A'][0]['b']).decode()
        dev['a'] = self.get_signed_hash(data['M'][0]['A'][0]['a']).decode()
        params['A'].append(dev)

        url = self.base_url + '/send'

        headers = {
            'User-Agent': 'SignalR (lang=Java; os=linux; version=2.0)',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        params = 'data=' + urllib.parse.quote_plus(json.dumps(params))
        self.sign_response = requests.post(
            url, data=params,  verify=ca_bundle,
            params=self.params, headers=headers)

    def get_signed_hash(self, hash):
        certificates = self.get_certificates()
        d = certificates['sign']['priv_key'].sign(
            b64decode(hash), mechanism=Mechanism.SHA256_RSA_PKCS)
        return b64encode(d)


"""
from client_fva.fva_speaker import FVA_client
c = FVA_client()
response = c.start()
c.process_messages(response)
"""
