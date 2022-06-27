import socket
import getpass

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Connecting to server...')
s.connect(('192.168.3.199', 4582))
username = input('Username: ').encode()
passwd = getpass.getpass().encode()
s.send(username + b':' + passwd)
while True:
    cmd = input('VNC Manager: ')
    if not cmd == '':
        s.send(cmd.encode())
        print(s.recv(1024).decode('utf-8'))
    if cmd == 'exit':
        break
