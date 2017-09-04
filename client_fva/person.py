'''
Created on 1 ago. 2017

@author: luis
'''
import requests
import json
import time
from datetime import datetime
from base64 import b64encode, b64decode

from . import Settings
from .rsa import get_hash_sum, encrypt
from client_fva.pkcs11client import PKCS11Client
from client_fva.rsa import decrypt


class PersonClientInterface():
    """
    .. note:: Este cliente está en desarrollo por lo que muchas cosas falta y muchos errores no son manejados
    así que cualquier aporte o revisión es bienvenida.

    Permite comunicar un programa en python con DFVA simplificando todos los procesos de encrypción de los datos,
    y acceso a los dispositivos PKCS11.

    Para hacer uso del cliente primero importe `PersonClient` el cual es un alias de `PKCS11PersonClient` quien es el que maneja 
    la comunicación con la tarjeta de firma digital.

    Para hacer uso de este software primero debe registrar como variabes de entorno lo siguiente

    .. code:: bash

        export PKCS11_PIN=<pin>
        export PKCS11_MODULE='<somepath>/dfva_client/clients/lib/x86_64/libASEP11.so'

    Aunque el cliente puede detectar los módulos y pedirá el pin en la consola, el método de variables de entorno es más rápido.

    Para iniciar a usar el cliente debe primero hacer lo siguiente 

    .. code:: python

        from clients.person import PersonClient
        client = PersonClient(person='04-0212-0119', slot=None)

    Dos parámetros muy importantes son: **person:** Cédula de identidad de la persona usuaria 
    (obligatorio de momento *espero poder leerlo del certificado*) y 
    **slot:** un slot corresponde a una lectora de tarjetas conectada (no estoy seguro si con tarjeta dentro).

    Una máquina puede tener muchas lectoras de tarjetas, pero este cliente solo maneja 1 tarjeta a la vez, 
    por lo que dar soporte a múltiples lectoras es tan simple como crear múltiples clientes 
    y pasar el parámetro slot a cada una.
    Para saber cómo detectar un slot ver get_slot() el cual supone al menos 1 slot conectado y 
    solo debe usarse para pruebas

    Sobre el transporte del material encriptado, actualmente se está realizando usando 
    RSA para encriptar el token de sessión para el algoritmo AES.MODE_EAX de encrypción simétrica

    .. note:: Con RSA la cantidad de información encriptada está limitada al tamaño de la llave privada y no se 
    puede encadenar multiples encripciones, por ello se usa AES, que es seguro si la llave de sessión está asegura. 

    .. note:: Esta interfaz describe todos los métodos disponibles del cliente en python.
    """

    def __init__(self, *args, **kwargs):
        """
        Inicializa el cliente con los parámetros proporcionados.

        * slot:  Lectora digital
        * person: Persona usuaria (debe coincidir con el dueño de la firma digital)
        * wait_time: Para los métodos donde se requiere espera activa (autenticación y firma) indica
        la cantidad de segundos a esperar entre llamados de consulta de estado
        * settings: Corresponde al archivo de preferencias de la aplicación, actualmente es una hoja de urls
        """

        pass

    def register(self):
        """
        Registra a la persona con el DFVA, puede pensarse como un sistema de login, lo que hace es:
        El cliente firma la solicitud con la cédula como clave, DFVA verifica que la cédula de la persona sea el 
        mensaje firmado, si lo es entonces le retorna un código encryptado con la llave pública, que solo puede ser
        desencryptado con la llave privada dentro de la lectora.

        Producto del proceso de firma, este método también inicia una session en la lectora digital si 
        todavía no se ha creado una.
        """
        pass

    def unregister(self):
        """Cierra la sessión dentro de la tarjeta, a futuro notificará a DFVA para que elimine el token"""
        pass

    def authenticate(self, identification, algorithm='sha512', wait=False):
        """Solicita una autenticación a la persona con la identificación suministrada"""
        pass

    def check_autenticate(self, identification, code, algorithm='sha512'):
        """Verifica si una solicitud de autenticación ya ha sido procesada.

        Cuando se solicita una autenticación el sistema devuelve un código que debe mostrarse al usuario, 
        para verificar si el usuario ya ingresó los datos debe usarse es mismo código y la misma identificación.
        """
        pass

    def sign(self, identification, document, algorithm='sha512',
             file_path=None, _format='xml', is_base64=False,
             wait=False):
        """Solicita la firma de un documento.

        Parámetros:

        * identification: identificación de la persona que debe firmar
        * document: Documento a firmar en base64 o None si se especifica file_path
        * file_path: Ruta del documento a firmar, acá el cliente se encarga de convertirlo a base64
        * _format: Corresponde al formato del documento a firmar, actualmente se puede firmar xml, odf, msoffice
        * is_base64: si document no es None y no está base64 (ej un archivo creados al vuelo o un buffer) se le puede perdir al 
        cliente que lo convierta a base64 
        """
        pass

    def check_sign(self, identification, code):
        """Verifica si una solicitud de firma ya ha sido procesada.

        Cuando se solicita una firma el sistema devuelve un código que debe mostrarse al usuario, 
        para verificar si el usuario ya ingresó los datos debe usarse es mismo código y la misma identificación.
        """
        pass

    def validate(self, document, file_path=None, algorithm='sha512', _format='certificate',
                 is_base64=False):
        """
        Verifica si un certificado o documento firmado está adecuadamente firmado y es válido.

        Parámeteros:

        * document: Documento a validar en base64 o None si se especifica file_path
        * file_path: Ruta del documento o certificado a valiad, acá el cliente se encarga de convertirlo a base64
        * _format: tipo de documento o certificado, los valores son 'certificate', 'xml', (actualmente el BCCR solo
        soporta estos, pero se espera que en un furturo cercano soporte odf, msoffice.
        * is_base64: si document no es None y no está base64 (ej un archivo creados al vuelo o un buffer) se le puede perdir al 
        cliente que lo convierta a base64 

        """

        pass

    def is_suscriptor_connected(self, identification, algorithm='sha512'):
        """Comprueba si un suscriptor (persona) está conectada con su dispositivo de firma digital.
        Puede usarse este método para indicarle al usuario cuando desea enviar una petición a firmar el estado de 
        la otra persona.
        """
        pass


class PersonBaseClient(PersonClientInterface):

    def _encrypt(self, str_data, etype='authenticate'):
        """ Encrypta usando alguno de los 2 encryptadores del dispositivo PKCS11.
        * etype = authenticate, sign
        """
        pass

    def _decrypt(self, str_data):
        """ Desencripta usando la llave privada del certificados de autenticación del dispositivo PKCS11.
        """
        pass

    def _get_public_auth_certificate(self):
        """Obtiene el certificado de autenticación de la tarjeta"""
        pass

    def _get_public_sign_certificate(self):
        """Obtiene el certificado de firma de la tarjeta"""
        pass

    def _get_time(self):
        # Fixme: sincronizar con timezone de CR y no usar el reloj de la
        # computadora
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def authenticate(self, identification, wait=False, algorithm='sha512'):
        data = {
            'person': self.person,
            'identification': identification,
            'request_datetime': self._get_time(),
        }

        str_data = json.dumps(data)
        edata = self._encrypt(str_data, etype='authenticate')
        hashsum = get_hash_sum(edata,  algorithm)
        edata = edata.decode()
        params = {
            "data_hash": hashsum,
            "algorithm": algorithm,
            "public_certificate": self._get_public_auth_certificate(),
            'person': self.person,
            "data": edata,
        }
        result = self.requests.post(
            self.settings.FVA_SERVER_URL +
            self.settings.AUTHENTICATE_PERSON, json=params)

        data = result.json()
        data = self._decrypt(data['data'])
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
        edata = self._encrypt(str_data, etype='authenticate')
        hashsum = get_hash_sum(edata,  algorithm)
        edata = edata.decode()
        params = {
            "data_hash": hashsum,
            "algorithm": algorithm,
            "public_certificate": self._get_public_auth_certificate(),
            'person': self.person,
            "data": edata,
        }
        result = self.requests.post(
            self.settings.FVA_SERVER_URL +
            self.settings.CHECK_AUTHENTICATE_PERSON % (code,), json=params)

        data = result.json()
        data = self._decrypt(data['data'])
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
        edata = self._encrypt(str_data, etype='sign')
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

        result = self.requests.post(
            self.settings.FVA_SERVER_URL + self.settings.SIGN_PERSON,
            json=params, headers=headers)

        data = result.json()
        data = self._decrypt(data['data'])
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
        edata = self._encrypt(str_data, etype='sign')
        hashsum = get_hash_sum(edata,  algorithm)
        edata = edata.decode()
        params = {
            "data_hash": hashsum,
            "algorithm": algorithm,
            "public_certificate": self._get_public_sign_certificate(),
            'person': self.person,
            "data": edata,
        }
        result = self.requests.post(
            self.settings.FVA_SERVER_URL +
            self.settings.CHECK_SIGN_PERSON % (code,), json=params)

        data = result.json()
        data = self._decrypt(data['data'])
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
        edata = self._encrypt(str_data, etype='sign')
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

        result = self.requests.post(
            self.settings.FVA_SERVER_URL + url, json=params, headers=headers)

        data = result.json()
        data = self._decrypt(data['data'])
        return data

    def is_suscriptor_connected(self, identification, algorithm='sha512'):

        data = {
            'person': self.person,
            'identification': identification,
            'request_datetime': self._get_time(),
        }

        str_data = json.dumps(data)
        edata = self._encrypt(str_data, etype='authenticate')
        hashsum = get_hash_sum(edata,  algorithm)
        edata = edata.decode()
        params = {
            "data_hash": hashsum,
            "algorithm": algorithm,
            "public_certificate": self._get_public_auth_certificate(),
            'person': self.person,
            "data": edata,
        }
        result = self.requests.post(
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


class PKCS11PersonClient(PKCS11Client, OSPersonClient):
    session = None
    certificates = None
    key_token = None
    info = None

    def __init__(self, *args, **kwargs):

        self.requests = kwargs.get('request_client', requests)
        self.wait_time = kwargs.get('wait_time', 10)
        self.settings = kwargs.get('settings', Settings())
        PKCS11Client.__init__(self, *args, **kwargs)

        self.person = self.get_person()

        if self.person is None:
            raise Exception(
                "Person can not be created, sorry read certificates fail")

        #self.session = self.get_session()
        #self.certificates = self.get_certificates()

    def get_person(self):
        return self.get_identification()

    def _get_public_auth_certificate(self):
        certificates = self.get_certificates()
        return certificates['authentication'].decode()

    def _get_public_sign_certificate(self):
        certificates = self.get_certificates()
        return certificates['sign'].decode()

    def get_key_token(self):
        """Convierte a texto plano o número el token de sessión de DFVA que está encriptado"""
        if self.key_token is None:
            self.register()

        keys = self.get_keys()
        key_token = keys['authentication']['priv_key'].decrypt(
            self.key_token)

        return key_token

    def _encrypt(self, str_data, etype='authenticate'):
        """
        etype = authenticate, sign
        """
        if etype == 'authenticate':
            etype = 'authentication'
        keys = self.get_keys()
        keytoken = self.get_key_token()
        signed_token = keys[etype]['priv_key'].sign(keytoken)
        return encrypt(keytoken, signed_token, str_data)

    def _decrypt(self, str_data):
        etype = 'authentication'
        keys = self.get_keys()
        return decrypt(keys[etype]['priv_key'], str_data)

    def sign_identification(self, identification):
        """Firma con la llave privada la identificación de la persona, para determinar si es correctamente, la 
        persona que dice ser (validación en DFVA).
        """
        keys = self.get_keys()
        return keys['authentication']['priv_key'].sign(identification)

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

        result = self.requests.post(
            self.settings.FVA_SERVER_URL +
            self.settings.LOGIN_PERSON, json=params)
        data = result.json()
        self.key_token = b64decode(data['token'])
        return data

    def unregister(self):
        if self.session:
            self.session.close()


PersonClient = PKCS11PersonClient
