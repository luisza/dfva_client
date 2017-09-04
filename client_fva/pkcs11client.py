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


class PKCS11Client:
    slot = None
    certificates = None
    key_token = None
    info = None
    settings = None
    keys = None

    def __init__(self, *args, **kwargs):

        self.settings = kwargs.get('settings', {})
        self.slot = kwargs.get('slot', self.get_slot())

    def get_slot(self):
        """Obtiene el primer slot (tarjeta) disponible
        .. warning:: Solo usar en pruebas y mejorar la forma como se capta
        """
        if self.slot:
            return self.slot

        lib = pkcs11.lib(self.get_module_lib())
        slots = lib.get_slots()
        if not slots:
            raise Exception("PKCS11: Slot not found")
        self.slot = slots[0]
        return self.slot

    def get_module_lib(self):
        """Obtiene la biblioteca de comunicación con la tarjeta """

        if 'PKCS11_MODULE' in self.settings:
            return self.settings['PKCS11_MODULE']

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
                BASE_DIR, 'client_fva/libs/%s/libASEP11.so' % (arch, ))
            if os.path.exists(path):
                return path
        except Exception as e:
            raise Exception(
                "Sorry not PKCS11 module found, please use export PKCS11_MODULE='<path>' before call python ")

    def get_pin(self, pin=None):
        """Obtiene el pin de la tarjeta para iniciar sessión"""

        if pin:
            return pin

        if 'PKCS11_PIN' in os.environ:
            return os.environ['PKCS11_PIN']
        else:  # FIXME: remove this line or send a signal
            return input("Write your pin: ")

        raise Exception(
            'Sorry PIN is Needed, we will remove this, but for now use export PKCS11_PIN=<pin> before call python')

    def get_session(self, pin=None):
        """Obtiene o inicializa una sessión para el uso de la tarjeta.
        .. warning:: Ojo cachear la session y revisar si está activa
        """
        # Fixme: Verificar si la sessión está activa y si no lo está entonces
        # volver a iniciarla
        if self.session is None:
            self.token = self.slot.get_token()
            self.session = self.token.open(user_pin=self.get_pin(pin=pin))
            return self.session
        return self.session

    def get_certificates(self):
        if self.certificates:
            return self.certificates

        slot = self.get_slot()
        certs = []
        token = slot.get_token()
        with token.open() as session:
            for cert in session.get_objects({
                    Attribute.CLASS: ObjectClass.CERTIFICATE}):
                x509 = OpenSSL.crypto.load_certificate(
                    OpenSSL.crypto.FILETYPE_ASN1, cert[Attribute.VALUE])
                certs.append(OpenSSL.crypto.dump_certificate(
                    OpenSSL.crypto.FILETYPE_PEM, x509))

        # FIXME: not positional extraction
        self.certificates = {
            'authentication': certs[0],
            'sign': certs[1]
        }
        return self.certificates

    def get_certificate_info(self):

        info = []
        slot = self.get_slot()
        token = slot.get_token()
        with token.open() as session:
            for cert in session.get_objects({
                    Attribute.CLASS: ObjectClass.CERTIFICATE}):
                x509 = OpenSSL.crypto.load_certificate(
                    OpenSSL.crypto.FILETYPE_ASN1, cert[Attribute.VALUE])
                subject = x509.get_subject()
                name = "%s %s" % (subject.GN, subject.SN)
                identification = subject.serialNumber
                person = {
                    'name': name.title(),
                    'identification': identification.replace("CPF-", ''),
                    'type': subject.O,
                    'organization': subject.OU,
                    'country': subject.C,
                    'commonName': subject.commonName,
                    'serialNumber': subject.serialNumber,
                    'cert_serialnumber': x509.get_serial_number(),
                    'cert_start': parse(x509.get_notBefore()),
                    'cert_expire': parse(x509.get_notAfter())
                }
                info.append(person)

        return info

    def get_keys(self, pin=None):
        """Extrae los certificados dentro del dispositivo y los guarda de forma estructurada para simplificar el acceso"""

        if self.keys is None:

            self.keys = {}
            session = self.get_session(pin=pin)
            certs = list(session.get_objects({
                Attribute.CLASS: ObjectClass.CERTIFICATE}))
            for cert in certs:
                x509 = OpenSSL.crypto.load_certificate(
                    OpenSSL.crypto.FILETYPE_ASN1, cert[Attribute.VALUE])
                objs = {
                    'pub_key': OpenSSL.crypto.dump_publickey(
                        OpenSSL.crypto.FILETYPE_PEM, x509.get_pubkey()),
                    'priv_key': list(session.get_objects({Attribute.CLASS: ObjectClass.PRIVATE_KEY,
                                                          Attribute.LABEL: cert[3]}))[0]
                }

                subject = x509.get_subject()
                if 'AUTENTICACION' in subject.CN:
                    self.keys['authentication'] = objs
                elif 'FIRMA' in subject.CN:
                    self.keys['sign'] = objs
                else:
                    print("ERROR:", objs)

        return self.keys

    def get_identification(self):
        info = self.get_certificate_info()
        person = None
        if info:
            person = info[0]['identification']
        return person
