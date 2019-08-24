import getpass
import os

import sleekxmpp
from sleekxmpp.exceptions import IqError, IqTimeout


class RegisterBot(sleekxmpp.ClientXMPP):
    def __init__(self, jid, password):
        sleekxmpp.ClientXMPP.__init__(self, jid,
                                      password)  # Nos conectamos con el cliente con el jid y el password que le pasamos

        self.add_event_handler('session_start', self.start, threaded=True)
        self.add_event_handler('register', self.register, threaded=True)  # Funcion del registro

        # 'session_start' y 'register': Son funciones predeterminadas de sleek

    def start(self, event):
        self.send_presence()

        self.disconnect()

    def register(self, iq):
        resp = self.Iq()
        resp['type'] = 'set'
        resp['register'][
            'username'] = self.boundjid.user  # Cuando nos conectamos, podemos acceder a nuestro usuario con: boundjid.user
        resp['register']['password'] = self.password  # Password

        try:
            resp.send(now=True)  # Enviamos los datos
            print('Cuenta creada exitosamesnte %s' % self.boundjid)  # Mensaje de: usuario registrado
        except IqError as e:
            print('Error al registrar la cuenta %s' % e.iq['error']['text'])
        except IqTimeout:
            print('El servidor no responde')
            self.disconnect()


if __name__ == '__main__':
    usuario = input("Username: ")
    password = getpass.getpass("Password: ")
    print('Seguro que desea registrar %s' % usuario)
    os.system("Pause")
    xmpp = RegisterBot(usuario, password)
    xmpp.register_plugin('xep_0030')
    xmpp.register_plugin('xep_0004')
    xmpp.register_plugin('xep_0066')
    xmpp.register_plugin('xep_0077')
    xmpp['xep_0077'].force_registration = True

    if xmpp.connect():
        xmpp.process(block=True)
    else:
        print('Error al conectar con el cliente')
