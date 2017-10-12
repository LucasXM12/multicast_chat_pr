import json
import struct
import socket

multicast_addr = '224.0.0.1'
bind_addr = '0.0.0.0'
port = 666

send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ttl = struct.pack('b', 1)
send_sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

receive_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
membership = socket.inet_aton(multicast_addr) + socket.inet_aton(bind_addr)

receive_sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, membership)
receive_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

receive_sock.bind((bind_addr, port))


def sendMsg(msg):
    str_msg = json.dumps(msg)
    send_sock.sendto(str_msg.encode('utf-8'), (multicast_addr, port))


def changeUserName():
    return input('\nDigite o seu usuário: ').replace(' ', '_')


send_msg = {'user_name': changeUserName(), 'msg': ''}

while True:
    cmd = input('\n->')

    if cmd == '/mu':
        send_msg['user_name'] = changeUserName()
    elif cmd == '/s':
        cmd = input('\nDeseja sair?\nQualquer coisa para calcelar ou [s/S] para sair: ')
        if cmd.lower() == 's':
            quit()
    else:
        send_msg['msg'] = cmd
        sendMsg(send_msg)
