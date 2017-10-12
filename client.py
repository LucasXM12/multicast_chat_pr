import json
import socket

multicast_addr = '224.0.0.1'
bind_addr = '0.0.0.0'
port = 666


def sendMsg(msg):
    print(json.dumps(msg))


def changeUserName():
    return input('Digite o seu usuário: ').replace(' ', '_')


message = {'user_name': changeUserName(), 'msg': ''}

while True:
    cmd = input('\n->')

    if cmd == '/mu':
        message['user_name'] = changeUserName()
    elif cmd == '/s':
        cmd = input('\nDeseja sair?\nQualquer coisa para calcelar ou [s/S] para sair: ')
        if cmd.lower() == 's':
            quit()
    else:
        message['msg'] = cmd
        sendMsg(message)
