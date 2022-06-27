import socket
import getpass

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Connecting to server...')
server_ip_f = open('server_ip.conf')
server_ip = server_ip_f.read()
server_ip_f.close()
s.connect((server_ip, 4582))
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
