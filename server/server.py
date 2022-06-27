from flask import Flask, request
import uuid
import json
import threading
import cli_session_mgmt
import socket

app = Flask(__name__)
client_list = {}

@app.route('/add/<string:hostname>')
def add(hostname):
    mgmt_id = uuid.uuid4()
    global client_list
    client_list[request.remote_addr] = {'hostname': hostname, 'mgmt_id': mgmt_id}
    return mgmt_id

@app.route('/list_clients')
def list_clients():
    clients = json.dumps(client_list)
    return clients

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
