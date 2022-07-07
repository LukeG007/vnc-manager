import requests
import api_endpoint
import socket
import os

if not os.path.exists('server_ip.conf'):
    open('server_ip.conf', 'x').close()
    print('Server IP Not set')
else:
    server_ip_f = open('server_ip.conf')
    server_ip = server_ip_f.read()
    server_ip_f.close()
    hostname = socket.gethostname()

    r = requests.get('http://{}:4583/add/{}'.format(server_ip, hostname))

    api_endpoint.run_server(server_ip)
