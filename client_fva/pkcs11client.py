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

logger = logging.getLogger('dfva_client')


class PKCS11Client:
    slot = None
    certificates = None
    key_token = None
    info = None
    settings = None
    keys = None
    identification = None

    def __init__(self, *args, **kwargs):

        self.settings = kwargs.get('settings', {})
        self.signal = kwargs.get('signal', None)
        self.slot = kwargs.get('slot', self.get_slot())

    def get_slot(self):
        """Obtiene el primer slot (tarjeta) disponible
        .. warning:: Solo usar en pruebas y mejorar la forma como se capta
        """
        if self.slot:
            return self.slot
        try:
            lib = pkcs11.lib(self.get_module_lib())
            slots = lib.get_slots()
        except Exception as e:
            self.signal.send('notify', obj={
                'message': "La biblioteca instalada no funciona para leer las tarjetas, esto puede ser porque no ha instalado las bibliotecas necesarias o porque el sistema operativo no está soportado"
            })
            logger.error("Error abriendo dispositivos PKCS11 %r" % (e,))

        if not slots:
            raise Exception("PKCS11: Slot not found")
        self.slot = slots[0]
        return self.slot

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
                BASE_DIR, 'client_fva/libs/%s/%s/libASEP11.so' % (_os, _os_arch))
        elif _os == "darwin":
            path = os.path.join(
                BASE_DIR, 'client_fva/libs/macos/libASEP11.dylib')
        elif _os == "windows":
            path = os.path.join(
                BASE_DIR, 'client_fva/libs/windows/asepkcs.dll')

        if os.path.exists(path):
            return path

        self.signal.send('notify', obj={
            'message': "No existe una biblioteca instalada para leer las tarjetas, esto puede ser porque no ha instalado las bibliotecas necesarias o porque el sistema operativo no está soportado"
        })

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
            respobj = signals.get_signal_response(
                self.signal.send('pin', obj={
                    'serial': serial}))
            return respobj.response['pin']

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
        if self.identification is not None:
            return self.identification

        info = None
        try:
            info = self.get_certificate_info()
        except pkcs11.exceptions.TokenNotRecognised as e:
            self.signal.send('notify', obj={
                'message': "No se puede obtener la identificación de la persona, posiblemente porque la tarjeta está mal conectada"
            })
            logger.error("Tarjeta no detectada %r" % (e, ))
        if info:
            self.identification = info[0]['identification']
        return self.identification
