'''
Created on 21 ago. 2017

@author: luis
'''
import pkcs11
import os
from dateutil.parser import parse
from pkcs11.constants import Attribute
from pkcs11.constants import ObjectClass
import OpenSSL
import platform
from client_fva import signals
import logging
import datetime
logger = logging.getLogger('dfva_client')

class Token:
    serial=None
    def __init__(serial):
        self.serial = serial
    

class Slot:
    def __init__(self, serial):
        self.serial = serial
    
    def get_token(self):
        return Token(self.serial)        

class B:
    pass

class PKCS11Exception:
    TokenNotRecognised = B()

class dummypkcs11:
    exceptions=PKCS11Exception()

    def lib(self):
        class A:
            def get_slot(self):
                """Obtiene el primer slot (tarjeta) disponible
                .. warning:: Solo usar en pruebas y mejorar la forma como se capta
                """
                return [Slot(b'446015340194853967119918706694137765024581677'), 
                        Slot(b'446015340196629408544548422120241811584796718')]
        return A()

class PrivateKey:
    dirpath = None

    def __init__(dirpath):
        self.dirpath=dirpath 
    def sign(self, data):
        pass
        

class PKCS11Client:
    slot = None
    certificates = None
    key_token = None
    info = None
    settings = None
    keys = None
    identification = None
    session=None
    def __init__(self, *args, **kwargs):
        self.settings = kwargs.get('settings', {})


    def get_slot(self):
        """Obtiene el primer slot (tarjeta) disponible
        .. warning:: Solo usar en pruebas y mejorar la forma como se capta
        """
        return [Slot(b'446015340194853967119918706694137765024581677'), 
                Slot(b'446015340196629408544548422120241811584796718')]

    def get_module_lib(self):
        """Obtiene la biblioteca de comunicación con la tarjeta """
         return '/usr/lib/libASEP11.so'


    def get_pin(self, pin=None):
        """Obtiene el pin de la tarjeta para iniciar sessión"""
        return "889888"

    def get_session(self, pin=None):
        """Obtiene o inicializa una sessión para el uso de la tarjeta.
        .. warning:: Ojo cachear la session y revisar si está activa
        """
        return None

    def read_public_from_disc(dirpath):
        x509 = OpenSSL.crypto.load_certificate(
                    OpenSSL.crypto.FILETYPE_ASN1, open(dirpath).read())
        return OpenSSL.crypto.dump_publickey(OpenSSL.crypto.FILETYPE_PEM, x509.get_pubkey())

    def read_certificate_from_disc(dirpath)
        x509 = OpenSSL.crypto.load_certificate(
                    OpenSSL.crypto.FILETYPE_ASN1, open(dirpath).read())
        return OpenSSL.crypto.dump_certificate(
                    OpenSSL.crypto.FILETYPE_PEM, x509)

    def get_certificates(self):
        if self.certificates:
            return self.certificates

        self.certificates = {'sign':  self.read_certificate_from_disc('certs/sign.crt'), 
                            'authentication': self.read_certificate_from_disc('certs/auth.crt') }
        return self.certificates

    def get_certificate_info(self):
         return [ {'identification': '03-0449-0054', 
                   'type': 'PERSONA FISICA', 
                   'organization': 'CIUDADANO', 
                   'serialNumber': 'CPF-03-0449-0054', 
                   'cert_start': datetime.datetime(2017, 3, 17, 14, 8, 58),
                   'name': 'Marta Eugenia Solano Gutierrez', 
                   'cert_serialnumber': 446015340194853967119918706694137765024581677, 
                   'commonName': 'MARTA EUGENIA SOLANO GUTIERREZ (AUTENTICACION)',
                   'cert_expire': datetime.datetime(2021, 3, 16, 14, 8, 58), 
                   'country': 'CR'
                  }, 
                 {'identification': '03-0449-0054', 
                  'type': 'PERSONA FISICA',
                  'organization': 'CIUDADANO', 
                  'serialNumber': 'CPF-03-0449-0054', 
                  'cert_start': datetime.datetime(2017, 3, 17, 14, 8, 59 ),
                  'name': 'Marta Eugenia Solano Gutierrez', 
                  'cert_serialnumber': 446015340196629408544548422120241811584796718, 
                  'commonName': 'MARTA EUGENIA SOLANO GUTIERREZ (FIRMA)', 
                  'cert_expire': datetime.datetime(2021, 3, 16, 14, 8, 59 ), 
                  'country': 'CR'}
               ]

    def get_keys(self, pin=None):
        """Extrae los certificados dentro del dispositivo y los guarda de forma estructurada para simplificar el acceso"""

        self.keys = {'sign': {'pub_key': read_public_from_disc('certs/sign.crt'), 
    'priv_key': PrivateKey('certs/sign.key')}, 

    'authentication': {'pub_key': read_public_from_disc('certs/auth.crt'), 
    'priv_key': PrivateKey('certs/auth.key')}

}
        return self.keys

    def get_identification(self):
        return "03-0449-0054"
