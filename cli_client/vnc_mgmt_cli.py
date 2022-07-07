import socket
import getpass

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Connecting to server...')
server_ip_f = open('server_ip.conf')
server_ip = server_ip_f.read()
server_ip_f.close()
s.connect((server_ip, 4582))
invalid_credentials = True
while invalid_credentials:
    username = input('Username: ').encode()
    passwd = getpass.getpass().encode()
    s.send(username + b':' + passwd)
    resp = s.recv(1024).decode('utf-8')
    if resp == 'auth':
        invalid_credentials = False
        print('Logged in as {}'.format(username.decode('utf-8')))
    else:
        print(resp)
        print('Authentication Failed, try again')
while True:
    cmd = input('VNC Manager: ')
    if not cmd == '':
        s.send(cmd.encode())
        print(s.recv(1024).decode('utf-8'))
    if cmd == 'exit':
        break
