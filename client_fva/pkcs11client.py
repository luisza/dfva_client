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

import io
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP


class Token:
    serial=None
    def __init__(self, serial):
        self.serial = serial
    

class Slot:
    def __init__(self, serial):
        self.serial = serial
    
    def get_token(self):
        return Token(self.serial)        

class B:
    pass

class PKCS11Exception(Exception):
    TokenNotRecognised = Exception

class dummypkcs11:
    exceptions=PKCS11Exception()

    def lib(self, mod):
        class A:
            def get_slots(self):
                """Obtiene el primer slot (tarjeta) disponible
                .. warning:: Solo usar en pruebas y mejorar la forma como se capta
                """
                return [Slot(b'446015340194853967119918706694137765024581677'), 
                        Slot(b'446015340196629408544548422120241811584796718')]
        return A()

class PrivateKey:
    dirpath = None
    key_length=2048

    def __init__(self, dirpath):
        self.dirpath=dirpath
 
    def sign(self, message):
        key = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, open(self.dirpath).read())
        return OpenSSL.crypto.sign(key, message, "sha512")

    def decrypt(self, message):
        file_in = io.BytesIO(message)
        file_in.seek(0)
        private_key = RSA.import_key(open(self.dirpath).read())

        enc_session_key, nonce, tag, ciphertext = \
           [ file_in.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1) ]

        # Decrypt the session key with the public RSA key
        cipher_rsa = PKCS1_OAEP.new(private_key)
        session_key = cipher_rsa.decrypt(enc_session_key)
 
        return session_key

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

    def read_public_from_disc(self, dirpath):
        #x509 = OpenSSL.crypto.load_certificate(
        #            OpenSSL.crypto.FILETYPE_ASN1, open(dirpath).read())
        #return OpenSSL.crypto.dump_publickey(OpenSSL.crypto.FILETYPE_PEM, x509.get_pubkey())
        return open(dirpath, 'rb').read()

    def read_certificate_from_disc(self, dirpath):
#        x509 = OpenSSL.crypto.load_certificate(
#                    OpenSSL.crypto.FILETYPE_ASN1, open(dirpath).read())
#        return OpenSSL.crypto.dump_certificate(
#                    OpenSSL.crypto.FILETYPE_PEM, x509)

        return open(dirpath, 'rb').read()


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

        self.keys = {'sign': {'pub_key': self.read_public_from_disc('certs/sign.crt'), 
    'priv_key': PrivateKey('certs/sign.key')}, 

    'authentication': {'pub_key': self.read_public_from_disc('certs/auth.crt'), 
    'priv_key': PrivateKey('certs/auth.key')}

}
        return self.keys

    def get_identification(self):
        return "03-0449-0054"
