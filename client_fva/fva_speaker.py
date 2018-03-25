'''
Created on 17 ago. 2017

@author: luis
'''

import requests
import os
from client_fva.rsa import pem_to_base64
import json
import urllib
from base64 import b64decode, b64encode
from client_fva.pkcs11client import PKCS11Client
from pkcs11.mechanisms import Mechanism
from client_fva import signals
import logging
import time
from client_fva.user_settings import UserSettings
import pkcs11
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ca_bundle = os.path.join(BASE_DIR, 'libs/certs/ca_bundle.pem')
from threading import Thread
from blinker import signal

logger = logging.getLogger('dfva_client')


class FVA_Base_client(PKCS11Client):
    info = None
    certificates = None
    session = None
    slot = None
    stop = False

    def __init__(self, *args, **kwargs):
        self.signal = kwargs.get('signal', signal('dfva_client'))
        kwargs['signal'] = self.signal
        self.settings = kwargs.get('settings', UserSettings())
        kwargs['settings'] = self.settings

        PKCS11Client.__init__(self, *args, **kwargs)
        self.identification = self.get_identification()

class FVA_client(FVA_Base_client, Thread):
    def __init__(self, *args, **kwargs):

        FVA_Base_client.__init__(self, *args, **kwargs)
        Thread.__init__(self)
        self.internal_daemon = kwargs.get('daemon', True)

    def run(self):

        if self.identification is None:
            logger.error(
                "No se puede iniciar FVA_client, obtención de identificación no se realizó adecuadamente")
            return

        while self.internal_daemon:
           # data = self.start_client()
           # if data is not None:
           #     self.process_messages(data)
           # else:
           #     logger.info("Esperando para reconectar a " +
           #                 self.identification)
           #     time.sleep(self.settings.reconnection_wait_time)
           a=0
           time.sleep(self.settings.reconnection_wait_time)

    def close(self):
        self.internal_daemon = False
        self.response.connection.close()
        logger.info("Terminando FVA_client de " + self.identification)


class OSDummyClient:
    def __init__(self):
        self.client = FVA_client()
        self.client.start()
        self.client.signal.connect(self.request_pin_code)

    def request_pin_code(self, sender, **kw):
        obj = kw['obj']
        print("%s dice:\n\n" % (obj.data['M'][0]['A'][0]['d'], ))
        print(obj.data['M'][0]['A'][0]['c'])

        obj.response['pin'] = input('Insert your pin: ')
        obj.response['code'] = input('Insert the code: ')
        obj.response['rejected'] = False
        return obj



"""
from client_fva.fva_speaker import FVA_client
c = FVA_client()
response = c.start()
c.process_messages(response)


from client_fva.fva_speaker import OSDummyClient
client= OSDummyClient()

"""
