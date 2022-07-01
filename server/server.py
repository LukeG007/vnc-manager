from flask import Flask, request
import json
import threading
import cli_session_mgmt
import vnc_mgmt
import auth_cli
import sqlite3
import client_mgmt
import os
import socket

app = Flask(__name__)
client_sys = client_mgmt.ClientManagement()
auth = auth_cli.AuthenticationManagement()
vnc_sys = vnc_mgmt.VNCManagement(auth, client_sys)

@app.route('/add/<string:hostname>')
def add(hostname):
    return client_sys.add_client(hostname, request.remote_addr)

@app.route('/list_clients')
def list_clients():
    clients = json.dumps(client_sys.client_list)
    return clients

@app.route('/auth', methods=['POST'])
def authenticate():
    auth_key = dict(request.form)['auth'].split(':')
    auth.auth(auth_key[0], auth_key[1])

def manage_cli_session(conn):
    try:
        authentication = conn.recv(1024).decode('utf-8').split(':')
    except ConnectionResetError:
        print('Connection to client lost, closing thread')
    else:
        if not authentication == '':
            session = cli_session_mgmt.CLISessionManagement(authentication[0], authentication[1])
            while True:
                try:
                    cmd = conn.recv(1024).decode('utf-8')
                    if cmd == 'exit':
                        conn.close()
                        break
                    else:
                        resp = session.execute(cmd)
                        conn.send(resp.encode())
                except ConnectionResetError:
                    print('Connection to client lost, closing thread')
                    break
        else:
            print('Connection to client lost, closing thread')

def start_cli_mgmt():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 4582))
    s.listen()
    while True:
        print('Listening for CLI connections')
        conn, addr = s.accept()
        threading.Thread(target=manage_cli_session, args=[conn]).start()

if __name__ == '__main__':
    threading.Thread(target=start_cli_mgmt).start()
    app.run('0.0.0.0', port=4583)
