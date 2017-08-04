'''
Created on 1 ago. 2017

@author: luis
'''
import requests
from datetime import datetime
import json

import time
from . import Settings
from base64 import b64encode, b64decode
import pkcs11
import os

import OpenSSL
from pkcs11.constants import Attribute
from pkcs11.constants import ObjectClass
from clients.rsa import get_hash_sum, encrypt, pem_to_base64


class PersonClientInterface():

    def register(self):
        pass

    def unregister(self):
        pass

    def authenticate(self, identification, algorithm='sha512', wait=False):
        pass

    def check_autenticate(self, identification, code, algorithm='sha512'):
        pass

    def sign(self, identification, document, algorithm='sha512',
             file_path=None, _format='xml', is_base64=False,
             wait=False):
        pass

    def check_sign(self, identification, code):
        pass

    def validate(self, document, file_path=None, algorithm='sha512', _format='certificate',
                 is_base64=False):
        pass

    def is_suscriptor_connected(self, identification, algorithm='sha512'):
        pass


class PersonBaseClient(PersonClientInterface):

    def __init__(self, person, wait_time=10, settings=Settings):
        self.person = person
        self.wait_time = wait_time
        self.settings = settings()

    def _encript(self, str_data, etype='authenticate'):
        """
        etype = authenticate, sign
        """
        pass

    def _get_public_auth_certificate(self):
        pass

    def _get_public_sign_certificate(self):
        pass

    def _get_time(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def authenticate(self, identification, wait=False, algorithm='sha512'):
        data = {
            'person': self.person,
            'identification': identification,
            'request_datetime': self._get_time(),
        }

        str_data = json.dumps(data)
        edata = self._encript(str_data, etype='authenticate')
        hashsum = get_hash_sum(edata,  algorithm)
        edata = edata.decode()
        params = {
            "data_hash": hashsum,
            "algorithm": algorithm,
            "public_certificate": self._get_public_auth_certificate(),
            'person': self.person,
            "data": edata,
        }
        result = requests.post(
            self.settings.FVA_SERVER_URL +
            self.settings.AUTHENTICATE_PERSON, json=params)

        data = result.json()
        if wait:
            while not data['received_notification']:
                time.sleep(self.wait_time)
                data = self.check_autenticate(
                    identification, data['code'], algorithm=algorithm)

        return data

    def check_autenticate(self, identification, code, algorithm='sha512'):
        data = {
            'person': self.person,
            'identification': identification,
            'request_datetime': self._get_time(),
        }

        str_data = json.dumps(data)
        edata = self._encript(str_data, etype='authenticate')
        hashsum = get_hash_sum(edata,  algorithm)
        edata = edata.decode()
        params = {
            "data_hash": hashsum,
            "algorithm": algorithm,
            "public_certificate": self._get_public_auth_certificate(),
            'person': self.person,
            "data": edata,
        }
        result = requests.post(
            self.settings.FVA_SERVER_URL +
            self.settings.CHECK_AUTHENTICATE_PERSON % (code,), json=params)

        data = result.json()
        return data

    def sign(self, identification, document, resume, _format="xml",
             file_path=None, is_base64=False,
             algorithm='sha512', wait=False):
        if not is_base64:
            document = b64encode(document).decode()

        data = {
            'person': self.person,
            'document': document,
            'format': _format,
            'algorithm_hash': algorithm,
            'document_hash': get_hash_sum(document,  algorithm),
            'identification': identification,
            'resumen': resume,
            'request_datetime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        str_data = json.dumps(data)
        edata = self._encript(str_data, etype='sign')
        hashsum = get_hash_sum(edata,  algorithm)
        edata = edata.decode()
        params = {
            "data_hash": hashsum,
            "algorithm": algorithm,
            "public_certificate": self._get_public_sign_certificate(),
            'person': self.person,
            "data": edata,
        }

        headers = {'Accept': 'application/json',
                   'Content-Type': 'application/json'}

        result = requests.post(
            self.settings.FVA_SERVER_URL + self.settings.SIGN_PERSON,
            json=params, headers=headers)

        data = result.json()

        if wait:
            while not data['received_notification']:
                time.sleep(self.wait_time)
                data = self.check_sign(
                    identification, data['code'], algorithm=algorithm)

        return data

    def check_sign(self, identification, code, algorithm='sha512'):
        data = {
            'person': self.person,
            'identification': identification,
            'request_datetime': self._get_time(),
        }

        str_data = json.dumps(data)
        edata = self._encript(str_data, etype='sign')
        hashsum = get_hash_sum(edata,  algorithm)
        edata = edata.decode()
        params = {
            "data_hash": hashsum,
            "algorithm": algorithm,
            "public_certificate": self._get_public_sign_certificate(),
            'person': self.person,
            "data": edata,
        }
        result = requests.post(
            self.settings.FVA_SERVER_URL +
            self.settings.CHECK_SIGN_PERSON % (code,), json=params)

        data = result.json()
        return data

    def validate(self, document, file_path=None, algorithm='sha512',
                 is_base64=False,
                 _format='certificate'):

        if not is_base64:
            document = b64encode(document).decode()
        data = {
            'person': self.person,
            'document': document,
            'request_datetime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        str_data = json.dumps(data)
        # print(str_data)
        edata = self._encript(str_data, etype='sign')
        hashsum = get_hash_sum(edata,  algorithm)
        edata = edata.decode()
        params = {
            "data_hash": hashsum,
            "algorithm": algorithm,
            "public_certificate": self._get_public_sign_certificate(),
            'person': self.person,
            "data": edata,
        }

        if _format == 'certificate':
            url = self.settings.VALIDATE_CERTIFICATE
        else:
            url = self.settings.VALIDATE_DOCUMENT
        headers = {'Accept': 'application/json',
                   'Content-Type': 'application/json'}

        result = requests.post(
            self.settings.FVA_SERVER_URL + url, json=params, headers=headers)

        return result.json()

    def is_suscriptor_connected(self, identification, algorithm='sha512'):

        data = {
            'person': self.person,
            'identification': identification,
            'request_datetime': self._get_time(),
        }

        str_data = json.dumps(data)
        edata = self._encript(str_data, etype='authenticate')
        hashsum = get_hash_sum(edata,  algorithm)
        edata = edata.decode()
        params = {
            "data_hash": hashsum,
            "algorithm": algorithm,
            "public_certificate": self._get_public_auth_certificate(),
            'person': self.person,
            "data": edata,
        }
        result = requests.post(
            self.settings.FVA_SERVER_URL +
            self.settings.SUSCRIPTOR_CONNECTED, json=params)

        data = result.json()
        dev = False
        if 'is_connected' in data:
            dev = data['is_connected']
        return dev


class OSPersonClient(PersonBaseClient):
    def sign(self, identification, document, resume, _format="xml",
             file_path=None, is_base64=False,
             algorithm='sha512', wait=False):

        if _format not in self.settings.SUPPORTED_SIGN_FORMAT:
            raise Exception("Format not supported only %s" %
                            (",".join(self.settings.SUPPORTED_SIGN_FORMAT)))

        if file_path is None and document is None:
            raise Exception("Document or file_path must be set")

        if file_path:
            with open(file_path, 'rb') as arch:
                document = arch.read()

        if hasattr(document, 'read'):
            document = document.read()

        # if hasattr(document, 'decode'):
        #    document = document.decode()

        if resume is None:
            resume = "Sorry document with out resume"

        return super(OSPersonClient, self).sign(
            identification,
            document,
            resume,
            _format=_format,
            file_path=None,
            is_base64=is_base64,
            algorithm=algorithm,
            wait=wait)

    def validate(self, document, file_path=None, algorithm='sha512',
                 is_base64=False,
                 _format='certificate'):

        if _format not in self.settings.SUPPORTED_VALIDATE_FORMAT:
            raise Exception("Format not supported only %s" %
                            (",".join(self.settings.SUPPORTED_VALIDATE_FORMAT)))

        if file_path is None and document is None:
            raise Exception("Document or file_path must be set")

        if file_path:
            with open(file_path, 'rb') as arch:
                document = arch.read()

        if hasattr(document, 'read'):
            document = document.read()

        return super(OSPersonClient, self).validate(
            document,
            file_path=None,
            algorithm=algorithm,
            is_base64=is_base64,
            _format=_format)


class PKCS11PersonClient(OSPersonClient):
    session = None
    certificates = None
    key_token = None

    def __init__(self, slot=None, person=None, wait_time=10, settings=Settings):
        if slot:
            self.slot = slot
        else:
            self.slot = self.get_slot()

        self.wait_time = wait_time
        self.settings = settings()
        self.person = person
        self.session = self.get_session()
        self.certificates = self.get_certificates()

    def get_module_lib(self):
        return os.environ['PKCS11_MODULE']

    def get_pin(self):
        return os.environ['PKCS11_PIN']

    def get_slot(self):
        """
        .. warning:: Solo usar en pruebas y mejorar la forma como se capta
        """
        lib = pkcs11.lib(self.get_module_lib())
        slots = lib.get_slots()
        if not slots:
            raise Exception("PKCS11: Slot not found")
        return slots[0]

    def get_session(self):
        """
        .. warning:: Ojo cachear la session y revisar si está activa
        """
        if self.session is None:
            self.token = self.slot.get_token()
            session = self.token.open(user_pin=self.get_pin())
            return session
        return self.session

    def get_certificates(self):
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

    def _get_public_auth_certificate(self):
        certificates = self.get_certificates()
        return certificates['authentication']['pem'].decode()

    def _get_public_sign_certificate(self):
        certificates = self.get_certificates()
        return certificates['sign']['pem'].decode()

    def get_key_token(self):
        if self.key_token is None:
            self.register()

        certificates = self.get_certificates()
        key_token = certificates['authentication']['priv_key'].decrypt(
            self.key_token)

        return key_token

    def _encript(self, str_data, etype='authenticate'):
        """
        etype = authenticate, sign
        """
        if etype == 'authenticate':
            etype = 'authentication'
        certificates = self.get_certificates()
        keytoken = self.get_key_token()
        signed_token = certificates[etype]['priv_key'].sign(keytoken)
        return encrypt(keytoken, signed_token, str_data)

    def sign_identification(self, identification):
        certificates = self.get_certificates()
        return certificates['authentication']['priv_key'].sign(identification)

    def register(self, algorithm='sha512'):

        edata = self.sign_identification(self.person)
        hashsum = get_hash_sum(edata,  algorithm)
        edata = b64encode(edata).decode()
        params = {
            "data_hash": hashsum,
            "algorithm": algorithm,
            "public_certificate": self._get_public_auth_certificate(),
            'person': self.person,
            "code": edata,
        }

        result = requests.post(
            self.settings.FVA_SERVER_URL +
            self.settings.LOGIN_PERSON, json=params)
        data = result.json()
        self.key_token = b64decode(data['token'])
        return data

    def unregister(self):
        self.session.close()


PersonClient = PKCS11PersonClient
