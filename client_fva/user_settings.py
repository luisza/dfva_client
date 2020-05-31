import configparser
import os
import stat


class UserSettings:

    def __init__(self):
        self.font_size = 12
        self.font_family = 'Noto Sans'
        self.theme = 'Fusion'
        self.save_password_in_manager = False
        self.number_requests_before_fail = 2
        self.save_signed_docs_path = ''
        self.module_path = ''
        # Necesita agregar en interfaz
        self.reconnection_wait_time = 10  # segundos
        self.max_pin_fails = 3  # Número máximo de errores al poner el pin

        # No necesita agregar a interfaz

        self.bccr_fva_domain = 'https://www.firmadigital.go.cr'
        self.bccr_fva_url_negociation = "/wcfv2/Bccr.Firma.Fva.Hub/signalr/negotiate?clientProtocol=1.4&connectionData=%5B%7B%22name%22%3A%22administradordeclientes%22%7D%5D"
        self.bccr_fva_url_connect = "/%s/connect"
        self.user_agent = 'SignalR (lang=Java; os=linux; version=2.0)'

        # DFVA settings
        self.fva_server_url = 'http://localhost:8000'
        self.authenticate_person = '/authenticate/person/'
        self.check_authenticate_person = '/authenticate/%s/person_show/'
        self.sign_person = '/sign/person/'
        self.check_sign_person = '/sign/%s/person_show/'
        self.validate_certificate = '/validate/person_certificate/'
        self.validate_document = '/validate/person_document/'
        self.suscriptor_connected = '/validate/person_suscriptor_connected/'
        self.login_person = '/login/'
        self.supported_sign_format = ['xml_cofirma', 'xml_contrafirma','odf', 'msoffice']
        self.supported_validate_format = [
            'certificate', 'cofirma', 'contrafirma', 'odf', 'msoffice']
        # Cuánto se espera para verificar si una autenticación o firma se llevó a cabo
        self.check_wait_time = 10

        self.config = configparser.ConfigParser()
        self.settings_file_path = os.path.join(
            os.environ.get('HOME'), ".fva_client")
        self.settings_file_name = "client.conf"

    def save(self):
        self.config['APPEARANCE'] = {
            'font_size': self.font_size,
            'font_family': self.font_family,
            'theme': self.theme
        }
        self.config['SECURITY'] = {
            'save_password_in_manager': self.save_password_in_manager,
            'number_requests_before_fail': self.number_requests_before_fail,
            'save_signed_docs_path': self.save_signed_docs_path,
            'reconnection_wait_time': self.reconnection_wait_time,
            'max_pin_fails': self.max_pin_fails
        }

        self.config['MODULE'] = {
            'module_path': self.module_path
        }

        self.config['BCCR_FVA'] = {
            'bccr_fva_domain': self.bccr_fva_domain,
            'bccr_fva_url_negociation': self.bccr_fva_url_negociation.replace("%", "@@"),
            'bccr_fva_url_connect': self.bccr_fva_url_connect.replace("%", "@@"),
            'user_agent': self.user_agent
        }
        self.config['DFVA'] = {
            'fva_server_url': self.fva_server_url,
            'authenticate_person': self.authenticate_person,
            'check_authenticate_person': self.check_authenticate_person.replace("%", "@@"),
            'sign_person': self.sign_person,
            'check_sign_person': self.check_sign_person.replace("%", "@@"),
            'validate_certificate': self.validate_certificate,
            'validate_document': self.validate_document,
            'suscriptor_connected': self.suscriptor_connected,
            'login_person': self.login_person,
            'supported_sign_format': ",".join(self.supported_sign_format),
            'supported_validate_format': ",".join(self.supported_validate_format),
            'check_wait_time': self.check_wait_time
        }
        # create settings folder if it doesn't exist
        if not os.path.exists(self.settings_file_path):
            os.mkdir(self.settings_file_path)

        with open(os.path.join(self.settings_file_path, self.settings_file_name), "w") as configfile:
            self.config.write(configfile)
        os.chmod(os.path.join(self.settings_file_path, self.settings_file_name), stat.S_IRWXU)

    def load(self):
        self.config.read(os.path.join(
            self.settings_file_path, self.settings_file_name))
        for section in self.config.sections():
            for key, value in self.config[section].items():
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

    # This method above make settings to work as dict
    # but only accept attributes that are described in __init__()
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
