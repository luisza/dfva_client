'''
Created on 2 ago. 2017

Recordar export PKCS11_PIN=

@author: luis
'''
from client_fva.person import PersonClient
from blinker import signal
client = PersonClient(person='04-0212-0119', signal=signal('fva_client'))

### PKCS11 TEST ####
certs = client.get_certificate_info()
print(certs)
keys = client.get_keys()
print(keys)
certs = client.get_certificates()
print(certs)

## DFVA TEST ###
client.register()
client.authenticate('04-0212-0119')

client.authenticate('04-0212-0119', wait=True)
client.sign('08-0888-0888',  None, "Readme file test",
            file_path='README.md', wait=True)

client.validate(None, file_path='README.md')
client.validate(None, file_path='README.md', _format='cofirma')
client.is_suscriptor_connected('08-0888-0888')

client.unregister()
