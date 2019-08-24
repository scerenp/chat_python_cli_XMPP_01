import getpass

import sleekxmpp, sys
from sleekxmpp.exceptions import IqError, IqTimeout

usuario = input("Username: ")
password = getpass.getpass("Password: ")
destino = input("Destino: ")

# usuario = 'saucer@alumchat.xyz'
# password = 'abc123**'
print('Iniciar Chat con %s' % destino)
xmpp = sleekxmpp.ClientXMPP(usuario, password)
xmpp.connect()
xmpp.process(block=False)


def chat_send():
    while True:
        mensaje = str(input('>>>> '))  # Nuestro mensaje
        if mensaje == 'exit':
            break  # si escribimos exit, nos salimos del bucle
        xmpp.send_message(mto=destino, mbody=mensaje)  # Enviamos el mensaje
    xmpp.disconnect()  # Nos desconectamos
    sys.exit(1)  # Y salimos


def message(msg):
    if msg['type'] in ('chat', 'normal'):  # Recibimos los mensajes que nos mandan
        print('%s %s' % (msg['body'], msg['from'].bare))  # Mensaje y nombre de usuario de quien lo envia


try:
    xmpp.send_presence()
    xmpp.get_roster()  # Obtenemos el roster si el usuario existe
    xmpp.register_plugin('xep_0030')  # service discovery
    xmpp.register_plugin('xep_0004')  # date form
    xmpp.register_plugin('xep_0060')  # pubsub
    xmpp.register_plugin('xep_0199')
except IqError as err:
    print('Error %s' % err.iq['error']['condition'])
    xmpp.disconnect()
    sys.exit(1)
except IqTimeout:
    print('El servidor no responde. Tal vez el usuario no exista')
    xmpp.disconnect()
    sys.exit(1)

print('Conectado con %s' % destino)
xmpp._start_thread('chat_send', chat_send)  # Funcion para enviar los mensajes
xmpp.add_event_handler('message', message)  # Funcion para recibir los mensajes

# 'message': es una funcion de sleek predeterminada para recibir mensajes
