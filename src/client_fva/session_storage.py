from Crypto.Random import get_random_bytes

from client_fva.models.Alias import Alias


class SessionStorage(object):

    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if SessionStorage.__instance is None:
            SessionStorage()
        return SessionStorage.__instance

    def __init__(self):
        if SessionStorage.__instance is not None:
            raise Exception("UserSettings class is a singleton!")
        else:
            SessionStorage.__instance = self

        self.pkcs11_client = None
        self.parent_widget = None
        self.session_info = {}
        self.transactions = {}
        """  
        'serial': {
            'tabnumber': 0,
            'slot': 0,
            'identification': '888888',
            'session_key': None,
            'user': None,
            'personclient': None,
            'fvaspeaker': None,
            'alias': ""
        }
        """


        self.tabs = ['General']
        self.serials = ['nd']
        self.persons = [None]
        self.users = [None, ]
        self.session_key = get_random_bytes(16)
        self.last_layout = None

    def set_db(self, db):
        self.db = db
        self.alias = Alias(db=db)