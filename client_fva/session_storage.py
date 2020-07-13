
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
        self.tabs = ['General']
        self.serials = ['nd']
        self.persons = [None]
        self.users = [None,]