import json
import struct
import socket
import threading

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

receive_sock.settimeout(0)

receive_sock.bind((bind_addr, port))


def sendMsg(msg):
    str_msg = json.dumps(msg)
    send_sock.sendto(str_msg.encode('utf-8'), (multicast_addr, port))


def changeUserName():
    return input('\nDigite o seu usuário: ').replace(' ', '_')


def recieveMsg():
    while running:
        try:
            message, address = receive_sock.recvfrom(255)

            recv_msg = json.loads(message.decode("utf-8"))
            user_name = recv_msg['user_name']

            if ip != address[0] or user_name != send_msg['user_name']:
                print('\n' + user_name + '->' + recv_msg['msg'])
        except Exception as e:
            pass


global send_msg
send_msg = {'user_name': changeUserName(), 'msg': ''}

global running
running = True

global ip
ip = socket.gethostbyname(socket.gethostname())

t = threading.Thread(target=recieveMsg)
t.start()

while True:
    cmd = input('\n')

    if cmd == '/mu':
        send_msg['user_name'] = changeUserName()
    elif cmd == '/s':
        cmd = input('\nDeseja sair?\nQualquer coisa para calcelar ou [s/S] para sair: ')
        if cmd.lower() == 's':
            running = False
            quit()
    else:
        send_msg['msg'] = cmd
        sendMsg(send_msg)
