import configparser
import os
import stat
import logging
from pathlib import Path
import pathlib

class UserSettings:
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if UserSettings.__instance is None:
            UserSettings()
        return UserSettings.__instance

    def __init__(self):
        if UserSettings.__instance is not None:
            raise Exception("UserSettings class is a singleton!")
        else:
            UserSettings.__instance = self

        self.logging_level = logging.DEBUG
        self.logging_formatter = '%(levelname)s - %(message)s'
        self.font_size = 12
        self.font_family = 'Noto Sans'
        self.theme = 'Fusion'
        self.save_password_in_manager = False
        self.number_requests_before_fail = 3
        self.save_signed_docs_path = ''
        self.module_path = ''
        self.hide_on_close = True  # by default window is only minimized

        # managed directly by us, not setup by the user
        self.max_pin_fails = 3  # max number of errors when input the pin
        self.reconnection_wait_time = 40  # seconds
        self.bccr_fva_domain = 'https://www.firmadigital.go.cr'
        self.bccr_fva_url_negotiation = "/wcfv2/Bccr.Firma.Fva.Hub/signalr/negotiate?clientProtocol=1.4&connectionData=%5B%7B%22name%22%3A%22administradordeclientes%22%7D%5D"
        self.bccr_fva_url_connect = "/%s/connect"
        self.user_agent = 'SignalR (lang=Java; os=linux; version=2.0)'

        # DFVA settings
        self.fva_server_url = 'http://localhost:8000'
        self.authenticate_person = '/person/authenticate/'
        self.check_authenticate_person = '/person/authenticate/%s/'
        self.authenticate_delete = '/person/sign/%s/'
        self.sign_person = '/person/sign/'
        self.check_sign_person = '/person/sign/%s/'
        self.sign_delete = '/person/sign/%s/'
        self.validate_certificate = '/person/validate_certificate/'
        self.validate_document = '/person/validate_document/'
        self.suscriptor_connected = '/person/validate_suscriptor/%s/'
        self.login_person = '/login/'
        self.supported_sign_format = ['xml_cofirma', 'xml_contrafirma', 'odf', 'msoffice', 'pdf']
        self.supported_validate_format = ['certificate', 'cofirma', 'contrafirma', 'odf', 'msoffice', 'pdf']
        self.algorithm = 'sha512'
        # how much time to wait before the verification of the status of the sign or authentication request
        self.check_wait_time = 10
        self.start_fva_bccr_client = True
        self.config = configparser.ConfigParser()
        self.settings_file_path = str( Path.home() / ".fva_client" )
        self.settings_file_name = "client.conf"
        self.installation_path = None

        self.secret_auth_keys = {}
        # non-active wait time for the thread
        self.wait_for_scan_new_device = 30
        self.validate_supported_extensions = {
            'docx': 'msoffice', 'doc': 'msoffice', 'xls': 'msoffice', 'xlsx': 'msoffice', 'ppt': 'msoffice',
            'pptx': 'msoffice', 'xml': 'cofirma', 'pdf': 'pdf', 'pem': 'certificate', 'crt': 'certificate',
            'der': 'certificate', 'odt': 'odf', 'ods': 'odf', 'odp': 'odf', 'odg': 'odf', 'odf': 'odf',
            'xmlc': 'contrafirma'
        }
        self.file_supported_extensions = {
            'docx': 'msoffice', 'doc': 'msoffice', 'xls': 'msoffice', 'xlsx': 'msoffice', 'ppt': 'msoffice',
            'pptx': 'msoffice', 'xml': 'xml_cofirma', 'pdf': 'pdf',
            'odt': 'odf', 'ods': 'odf', 'odp': 'odf', 'odg': 'odf', 'odf': 'odf', 'xmlc': 'xml_contrafirma'
        }

    def get_installation_path(self):
        if self.installation_path:
            return self.installation_path
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def save(self):
        self.config['APPEARANCE'] = {
            'font_size': self.font_size,
            'font_family': self.font_family,
            'theme': self.theme
        }
        self.config['SECURITY'] = {
            'hide_on_close': self.hide_on_close,
            'save_password_in_manager': self.save_password_in_manager,
            'number_requests_before_fail': self.number_requests_before_fail,
            'save_signed_docs_path': self.save_signed_docs_path,
            'reconnection_wait_time': self.reconnection_wait_time,
            'max_pin_fails': self.max_pin_fails
        }
        self.config['BCCR_FVA'] = {
            'bccr_fva_domain': self.bccr_fva_domain,
            'bccr_fva_url_negotiation': self.bccr_fva_url_negotiation.replace("%", "@@"),
            'bccr_fva_url_connect': self.bccr_fva_url_connect.replace("%", "@@"),
            'user_agent': self.user_agent
        }
        self.config['DFVA'] = {
            'fva_server_url': self.fva_server_url,
            'authenticate_person': self.authenticate_person,
            'check_authenticate_person': self.check_authenticate_person.replace("%", "@@"),
            'authenticate_delete': self.authenticate_delete.replace("%", "@@"),
            'sign_person': self.sign_person,
            'check_sign_person': self.check_sign_person.replace("%", "@@"),
            'sign_delete': self.sign_delete.replace("%", "@@"),
            'validate_certificate': self.validate_certificate,
            'validate_document': self.validate_document,
            'suscriptor_connected': self.suscriptor_connected.replace("%", "@@"),
            'login_person': self.login_person,
            'supported_sign_format': ",".join(self.supported_sign_format),
            'supported_validate_format': ",".join(self.supported_validate_format),
            'check_wait_time': self.check_wait_time
        }
        self.config['DEVICES'] = {
            'wait_for_scan_new_device': self.wait_for_scan_new_device,
            'module_path': self.module_path
        }
        self.config['LOGGING'] = {
            'logging_formatter': self.logging_formatter.replace("%", "@@"),
            'logging_level': self.logging_level
        }

        # create settings folder if it doesn't exist
        if not os.path.exists(self.settings_file_path):
            os.mkdir(self.settings_file_path)

        with open(os.path.join(self.settings_file_path, self.settings_file_name), "w") as configfile:
            self.config.write(configfile)
        os.chmod(os.path.join(self.settings_file_path,
                              self.settings_file_name), stat.S_IRWXU)

    def get_home_path(self):
        if not os.path.exists(self.settings_file_path):
            os.mkdir(self.settings_file_path)
        return self.settings_file_path

    def serialize_tokens(self, text):
        data = text.split(';')
        for key in data:
            k, v = key.split(',')
            self.secret_auth_keys[k]=v

    def load(self):
        self.config.read(os.path.join(
            self.settings_file_path, self.settings_file_name))
        for section in self.config.sections():
            for key, value in self.config[section].items():
                if key == 'auth_token':
                    self.serialize_tokens(value)
                    continue

                value = value.replace("@@", "%")
                try:
                    typ = type(getattr(self, key))
                    if typ == bool:
                        value = self.config.getboolean(section, key)
                    if typ == list:
                        value = value.split(",")
                    setattr(self, key, typ(value))
                except Exception as e:
                    pass

    # methods to make the settings class to work like a dict, it only accepts those attributes setup in the __init__
    def __getitem__(self, key):
        if hasattr(self, key):
            return getattr(self, key)
        raise KeyError(key)

    def __setitem__(self, key, value):
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            raise KeyError(key)

    def __contains__(self, key):
        return hasattr(self, key)
