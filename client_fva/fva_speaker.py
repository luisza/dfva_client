'''
Created on 17 ago. 2017

@author: luis
'''

import requests
import os
import OpenSSL
from pkcs11.constants import Attribute
from pkcs11.constants import ObjectClass
import pkcs11
from client_fva.rsa import pem_to_base64
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ca_bundle = os.path.join(BASE_DIR, 'lib/certs/ca_bundle.pem')


class FVA_client:
    info = None
    certificates = None
    session = None
    slot = None

    def __init__(self):
        self.slot = self.get_slot()

    def start_the_negotiation(self):
        headers = {
            'User-Agent': 'SignalR (lang=Java; os=linux; version=2.0)'
        }

        url = "https://www.firmadigital.go.cr/wcfv2/Bccr.Firma.Fva.Hub/signalr/negotiate?clientProtocol=1.4&connectionData=%5B%7B%22name%22%3A%22administradordeclientes%22%7D%5D"
        response = requests.get(url, verify=ca_bundle, headers=headers)
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
        return response.json()

    def start_the_communication(self, data):
        print(data)
        certificates = self.get_certificates()
        con_data = "connectionData=[{\"name\":\"administradordeclientes\"}]"
        url_var = "%s/connect?connectionToken=%s&connectionId=%s" % (
            data['Url'],
            data['ConnectionToken'],
            data['ConnectionId'])

        url = """https://www.firmadigital.go.cr/%s&transport=serverSentEvents&%s
    """ % (
            url_var, con_data
        )

        uname = os.uname()
        print(
            repr(pem_to_base64(certificates['authentication']['pem'].decode())))
        headers = {
            'Accept': 'text/event-stream',
            'CertificadoAutenticacion': pem_to_base64(certificates['authentication']['pem'].decode()),
            'CertificadoFirmante': pem_to_base64(certificates['sign']['pem'].decode()),
            'NombreDelSistemaOperativo': uname[0],
            'VersionDelSistemaOperativo': uname[3],
            'IpPrivada': '192.168.1.2',
            'Arquitectura': 'amd64' if uname[4] == 'x86_64' else 'x86',
            'NombreDelHost': uname[1],
            'User-Agent': 'SignalR (lang=Java; os=linux; version=2.0)',
            'Content-Encoding': 'gzip'
        }

        self.response = requests.get(url, headers=headers,
                                     verify=ca_bundle,
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


"""
from client_fva.fva_speaker import FVA_client
c = FVA_client()
response = c.start()
response.raw.read(1024)

"""
