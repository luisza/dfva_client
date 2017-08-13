'''
Created on 2 ago. 2017

@author: luis
'''


from clientfva.person import PersonClient

client = PersonClient(person='04-0212-0119')
client.register()
client.authenticate('04-0212-0119')

client.authenticate('04-0212-0119', wait=True)
client.sign('08-0888-0888',  None, "Readme file test",
            file_path='README.md', wait=True)

client.validate(None, file_path='README.md')
client.validate(None, file_path='README.md', _format='xml')
client.is_suscriptor_connected('08-0888-0888')
