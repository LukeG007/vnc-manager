from flask import Flask, request
import uuid
import json

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

if __name__ == '__main__':
    app.run('0.0.0.0', port=4583)
