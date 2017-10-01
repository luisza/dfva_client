import configparser
import os


class UserSettings:

    def __init__(self):
        self.font_size = 10
        self.font_family = 'Noto Sans'
        self.theme = 'GTK+'
        self.save_password_in_manager = False
        self.number_requests_before_fail = 2
        self.save_signed_docs_path = ''
        self.module_path = ''
        self.config = configparser.ConfigParser()
        self.settings_file_path = os.path.join(os.environ.get('HOME'), ".fva_client")
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
            'save_signed_docs_path': self.save_signed_docs_path
        }
        self.config['MODULE'] = {
            'module_path': self.module_path
        }

        # create settings folder if it doesn't exist
        if not os.path.exists(self.settings_file_path):
            os.mkdir(self.settings_file_path)

        with open(os.path.join(self.settings_file_path, self.settings_file_name), "w") as configfile:
            self.config.write(configfile)

    def load(self):
        self.config.read(os.path.join(self.settings_file_path, self.settings_file_name))
        for section in self.config.sections():
            for key, value in self.config[section].items():
                try:
                    typ = type(getattr(self, key))
                    if typ == bool:
                        value = self.config.getboolean(section, key)
                    setattr(self, key, typ(value))
                except Exception as e:
                    pass
