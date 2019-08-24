# coding=utf-8
import getpass
import os

import sleekxmpp, sys
from sleekxmpp.exceptions import IqError, IqTimeout

usuario = input("Username: ")
password = getpass.getpass("Password: ")
print('Seguro desea eliminar %s' % usuario)
os.system("Pause")

xmpp = sleekxmpp.ClientXMPP(usuario, password)
xmpp.connect()
xmpp.process(block=False)

xmpp.register_plugin('xep_0077')

try:
    xmpp.plugin['xep_0077'].cancel_registration(ifrom=xmpp.boundjid.full)  # Procedemos a eliminar
    print('Cuenta eliminada exitosamente %s ' % xmpp.boundjid)
except IqError as e:
    print('Error: %s' % e.iq['error']['text'])
    xmpp.disconnect()
    sys.exit(1)
except IqTimeout:
    print('El servidor no responde')
    xmpp.disconnect()
    sys.exit(1)

xmpp.disconnect()
