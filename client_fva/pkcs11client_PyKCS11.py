'''
Created on 21 ago. 2017

@author: luis
'''
import PyKCS11
import os
import platform
from client_fva import signals
import logging
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.x509.oid import NameOID, ExtensionOID
from blinker import signal
import threading

logger = logging.getLogger('dfva_client')
certs_session_mutex = threading.Lock()


class PrivateKey:
    def __init__(self, key, client):
        self._key = key
        self._client = client
        self.key_length = self.get_key_length()

    def decrypt(self, ciphertext):
        session = self._client.get_session()
        mechanism = PyKCS11.Mechanism(PyKCS11.CKM_SHA1_RSA_PKCS, None)
        mech = PyKCS11.RSAOAEPMechanism(
            PyKCS11.CKM_SHA_1, PyKCS11.CKG_MGF1_SHA1)
        decrypted = bytes(
            bytearray(session.decrypt(self._key, ciphertext, mech)))
        return decrypted

    def sign(self, data, using='sha512'):
        if using == 'sha512':
            mechanism = PyKCS11.Mechanism(PyKCS11.CKM_SHA512_RSA_PKCS, None)
        elif using == 'sha256':
            mechanism = PyKCS11.Mechanism(PyKCS11.CKM_SHA256_RSA_PKCS, None)

        session = self._client.get_session()        
        signature = session.sign(self._key, data, mechanism)
        signature = bytes(bytearray(signature))
        return signature

    def get_key_length(self):
        session = self._client.get_session()
        moduslen = len(bytes(bytearray(
            session.getAttributeValue(self._key,
                                      [PyKCS11.CKA_MODULUS])[0])))
        return moduslen*8

    def key(self):
        return self._key


class PKCS11Client:
    def __init__(self, *args, **kwargs):
        self.slots = None
        self.token = None
        self.certificates = None
        self.key_token = None
        self.info = None
        self.keys = None
        self.session = None
        self.identification = kwargs.get('identification', None)
        self.cached = kwargs.get('cached', True)
        self.settings = kwargs.get('settings', {})
        self.pkcs11 = PyKCS11.PyKCS11Lib()
        self.slot = kwargs.get('slot', None)
        self.certificate_info = None

    def get_slot(self):
        """Obtiene el primer slot (tarjeta) disponible
        .. warning:: Solo usar en pruebas y mejorar la forma como se capta
        """
        if self.slot:
            return self.slot
        slots = self.get_slots()
        if not slots:
            raise Exception("PKCS11: Slot not found")
        self.slot = slots[0]
        return self.slot

    def get_slots(self):
        """Obtiene el primer slot (tarjeta) disponible
        .. warning:: Solo usar en pruebas y mejorar la forma como se capta
        """
        if self.slots is not None and self.cached:
            return self.slots
        try:
            self.pkcs11.load(self.get_module_lib())
            self.slots = self.pkcs11.getSlotList()
        except Exception as e:
            signals.send('notify', signals.SignalObject(
                signals.NOTIFTY_ERROR,
                {
                    'message': "La biblioteca instalada no funciona para leer \
                    las tarjetas, esto puede ser porque no ha instalado \
                    las bibliotecas necesarias o porque el sistema operativo \
                    no está soportado"
                })
            )
            logger.error("Error abriendo dispositivos PKCS11 %r" % (e,))
            return []
        return self.slots

    def get_token(self, slot):
        if self.token is not None and self.cached:
            return self.token
        self.token = None
        try:
            self.token = self.pkcs11.getTokenInfo(slot)
        except PyKCS11.PyKCS11Error as e:
            if e.value == PyKCS11.CKR_TOKEN_NOT_RECOGNIZED:
                logger.debug("Not token on slot " + repr(slot))
                self.token = None
            else:
                raise
        return self.token

    def get_tokens_information(self):
        slots = self.get_slots()
        dev = []
        for slot in slots:
            token = self.get_token(slot)
            if token is not None:
                dev.append({
                            'slot': slot,
                            'serial': token.serialNumber,
                            'label': token.label,
                            'model': token.model,
                            'manufacturer': token.manufacturerID
                        })
        return dev

    def get_module_lib(self):
        """Obtiene la biblioteca de comunicación con la tarjeta """

        if hasattr(self.settings, 'module_path') and self.settings.module_path:
            return self.settings.module_path

        if 'PKCS11_MODULE' in os.environ:
            return os.environ['PKCS11_MODULE']

        if os.path.exists('/usr/lib/libASEP11.so'):  # Linux
            return '/usr/lib/libASEP11.so'

        if os.path.exists("/usr/local/lib/libASEP11.dylib"):  # macOS
            return "/usr/local/lib/libASEP11.dylib"

        # FIXME: Hacer la construcción del path por defecto para windows,
        # sugerencia
        """
        public static String ObtenerDirectorioDeWindows()
          {
            String direccionDeWindows = System.getenv("SystemRoot");
            if ((direccionDeWindows == null) || (direccionDeWindows.equalsIgnoreCase(""))) {
              direccionDeWindows = System.getenv("WINDIR");
            }
            String directorioDeWindows = direccionDeWindows + File.separator + "system32";
            return directorioDeWindows;
          }
        """

        _os = platform.system().lower()
        _os_arch = platform.machine()
        BASE_DIR = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__)))
        if _os == 'linux':
            path = os.path.join(
                BASE_DIR, 'os_libs/%s/%s/libASEP11.so' % (_os, _os_arch))
        elif _os == "darwin":
            path = os.path.join(
                BASE_DIR, 'os_libs/macos/libASEP11.dylib')
        elif _os == "windows":
            path = os.path.join(
                BASE_DIR, 'os_libs/windows/asepkcs.dll')

        if os.path.exists(path):
            return path

        signals.send('notify', signals.SignalObject(
            signals.NOTIFTY_ERROR,
            {'message': "No existe una biblioteca instalada para leer las \
              tarjetas, esto puede ser porque no ha instalado las bibliotecas \
              necesarias o porque el sistema operativo no está soportado"
            })
        )

    def get_pin(self, pin=None):
        """Obtiene el pin de la tarjeta para iniciar sessión"""

        if pin:
            return pin

        if 'PKCS11_PIN' in os.environ:
            return os.environ['PKCS11_PIN']
        else:
            try:
                serial = self.get_slot().get_tokens()[0].serial.decode('utf-8')
            except:
                serial = 'N/D'
                # Fixme: aqui debería manejarse mejor
            respobj = signals.receive(
                signals.send('pin', signals.SignalObject(
                    signals.PIN_REQUEST,
                    {'serial': serial})
                )
            )
            return respobj.response['pin']

        raise Exception(
            'Sorry PIN is Needed, we will remove this, but for now use export \
            PKCS11_PIN=<pin> before call python')

    def is_session_active(self, session):
        dev = False
        if session is not None:
            try:
                info = session.getSessionInfo()
                if info.state == 1:
                    dev = True
            except PyKCS11.PyKCS11Error as e:
                dev = False
        return dev

    def get_session(self, pin=None):
        """Obtiene o inicializa una sessión para el uso de la tarjeta.
        .. warning:: Ojo cachear la session y revisar si está activa
        """
        # Fixme: Verificar si la sessión está activa y si no lo está entonces
        # volver a iniciarla

        if self.session is None or not self.is_session_active(self.session):
            slot = self.get_slot()
            token = self.get_token(slot)
            if token is not None:
                self.session = self.pkcs11.openSession(slot)
                self.session.login(self.get_pin(pin=pin))
                return self.session
            else:
                if self.session is not None:
                    self.session.closeSession()
                    self.session = None
        return self.session

    def get_certificates(self):
        if self.certificates and self.cached:
            return self.certificates

        slot = self.get_slot()
        certs = []
        token = self.get_token(slot)
        if token is not None:
            certs_session_mutex.acquire()
            session = self.pkcs11.openSession(slot)
            self.certificates = {}
            for cert in session.findObjects([(PyKCS11.CKA_CLASS,
                                            PyKCS11.CKO_CERTIFICATE)]):

                certdata = session.getAttributeValue(cert, [PyKCS11.CKA_VALUE])
                cert = x509.load_der_x509_certificate(
                    bytes(bytearray(certdata[0])),
                    default_backend())

                exkey = cert.extensions.get_extension_for_oid(
                    ExtensionOID.EXTENDED_KEY_USAGE)
                if exkey and any([x.dotted_string == '1.3.6.1.5.5.7.3.2' for x in exkey.value._usages]):
                    key = 'authentication'
                else:
                    key = 'sign'
                self.certificates[key] = cert.public_bytes(
                    serialization.Encoding.PEM)
            session.logout()
            session.closeSession()
            certs_session_mutex.release()
        return self.certificates

    def get_certificate_info(self):
        if self.certificate_info and self.cached:
            return self.certificate_info

        certs = self.get_certificates()
        if certs is not None:
            self.certificate_info = {}
            for key, certpem in certs.items():
                cert = x509.load_pem_x509_certificate(
                    certpem,
                    default_backend())
                GN = cert.subject.get_attributes_for_oid(
                    NameOID.GIVEN_NAME)[0].value
                SN = cert.subject.get_attributes_for_oid(NameOID.SURNAME)[
                    0].value
                O = cert.subject.get_attributes_for_oid(
                    NameOID.ORGANIZATION_NAME)[0].value
                OU = cert.subject.get_attributes_for_oid(
                    NameOID.ORGANIZATIONAL_UNIT_NAME)[0].value
                C = cert.subject.get_attributes_for_oid(
                    NameOID.COUNTRY_NAME)[0].value

                CN = cert.subject.get_attributes_for_oid(
                    NameOID.COMMON_NAME)[0].value
                name = "%s %s" % (GN,  SN)
                identification = cert.subject.get_attributes_for_oid(
                    NameOID.SERIAL_NUMBER)[0].value
                person = {
                    'name': name.title(),
                    'identification': identification.replace("CPF-", ''),
                    'type': O,
                    'organization': OU,
                    'country':  C,
                    'commonName': CN,
                    'serialNumber': identification,
                    'cert_serialnumber': str(cert.serial_number),
                    'cert_start': cert.not_valid_before,
                    'cert_expire': cert.not_valid_after
                }
                self.certificate_info[key] = person

        return self.certificate_info

    def get_keys(self, pin=None):
        """Extrae los certificados dentro del dispositivo y los guarda de forma 
        estructurada para simplificar el acceso"""

        if self.keys is None or not self.cached:
            self.keys = {
                'authentication': {
                    'pub_key': None,
                    'priv_key': None
                },
                'sign': {
                    'pub_key': None,
                    'priv_key': None
                },
            }
            session = self.get_session(pin=pin)
            if session is not None:
                certs = self.get_certificates()
                objkeys = session.findObjects([(PyKCS11.CKA_CLASS,
                                                PyKCS11.CKO_PRIVATE_KEY)])
                objpublickeys = session.findObjects(
                    [(PyKCS11.CKA_CLASS, PyKCS11.CKO_PUBLIC_KEY)])

                for pubkey in objpublickeys:
                    label = session.getAttributeValue(
                        pubkey, [PyKCS11.CKA_LABEL])[0]
                    if label == 'LlaveDeAutenticacion':
                        self.keys['authentication']['pub_key'] = pubkey
                    elif label == 'LlaveDeFirma':
                        self.keys['sign']['pub_key'] = pubkey

                for key in objkeys:
                    label = session.getAttributeValue(
                        key, [PyKCS11.CKA_LABEL])[0]
                    if label == 'LlaveDeAutenticacion':
                        self.keys['authentication']['priv_key'] = PrivateKey(
                            key, self)
                    elif label == 'LlaveDeFirma':
                        self.keys['sign']['priv_key'] = PrivateKey(key, self)
            else:
                self.keys = None
        return self.keys

    def get_identification(self):
        if self.identification is not None and self.cached:
            return self.identification

        info = None
        try:
            info = self.get_certificate_info()
            if info is None:
                raise Exception()
        except Exception as e:
            # FIXME: set a correct type of exception
            signals.send('notify', signals.SignalObject(
                signals.NOTIFTY_ERROR,
                {
                'message': "No se puede obtener la identificación de la persona\
                , posiblemente porque la tarjeta está mal conectada"
                })
            )
            logger.error("Tarjeta no detectada %r" % (e, ))
            raise
        if info:
            self.identification = info['authentication']['identification']
        return self.identification

    def pksc11_sign(data, key='sign', pin=None):
        mechanism = PyKCS11.Mechanism(PyKCS11.CKM_SHA1_RSA_PKCS, None)
        certs = self.get_keys(pin=pin)
        session = self.get_session(pin=pin)
        privKey = certs[key]['priv_key'].key()
        mechanism = PyKCS11.Mechanism(PyKCS11.CKM_SHA1_RSA_PKCS, None)
        signature = session.sign(privKey, data, mechanism)
        signature = bytes(bytearray(signature))
        return signature

    def pkcs11_decrypt(data, key='authentication', pin=None):
        certs = self.get_keys(pin=pin)
        session = self.get_session(pin=pin)
        privKey = certs[key]['priv_key'].key()
        mechanism = PyKCS11.Mechanism(PyKCS11.CKM_SHA1_RSA_PKCS, None)
        mech = PyKCS11.RSAOAEPMechanism(
            PyKCS11.CKM_SHA_1, PyKCS11.CKG_MGF1_SHA1)
        decrypted = bytes(
            bytearray(session.decrypt(privKey, ciphertext, mech)))
        return decrypted

    def close(self):
        if self.session:
            if self.is_session_active(self.session):
                self.session.logout()
            self.session.closeSession()
            self.session = None
            self.keys = None
            self.certificate_info = None
            self.certificates = None
