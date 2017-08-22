
class Settings(dict):
    FVA_SERVER_URL = 'http://localhost:8000'
    AUTHENTICATE_PERSON = '/authenticate/person/'
    CHECK_AUTHENTICATE_PERSON = '/authenticate/%s/person_show/'
    SIGN_PERSON = '/sign/person/'
    CHECK_SIGN_PERSON = '/sign/%s/person_show/'
    VALIDATE_CERTIFICATE = '/validate/person_certificate/'
    VALIDATE_DOCUMENT = '/validate/person_document/'
    SUSCRIPTOR_CONNECTED = '/validate/person_suscriptor_connected/'
    LOGIN_PERSON = '/login/'

    SUPPORTED_SIGN_FORMAT = ['xml', 'odf', 'msoffice']
    SUPPORTED_VALIDATE_FORMAT = ['certificate', 'xml', 'odf', 'msoffice']
