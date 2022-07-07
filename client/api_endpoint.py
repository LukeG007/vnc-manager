from flask import Flask, request
import requests

app = Flask(__name__)

def auth(auth):
    r = requests.post('http://{}:4583/auth', json={'auth': auth})
    authenticated = None
    if r.text == 'False':
        authenticated = False
    else:
        authenticated = int(r.text)
    return authenticated

def get_vnc_data():
    r = requests.get('http://{}/vnc_data'.format(app.server_ip))
    return r.json()

def start_vncserver(port):
    print('start_vncserver({}) called'.format(port))

@app.route('/start', methods=['POST'])
def start_vnc():
    data = dict(request.form)
    auth_details = data['auth']
    port = data['port']
    authenticated = auth(auth_details)
    if not authenticated == False:
        permissions = authenticated
        vnc_data = get_vnc_data()
        if port in vnc_data:
            if permissions == 0:
                if auth_details.split(':')[0] == vnc_data[port]['username']:
                    start_vncserver()
                else:
                    return 'unprivileged'
            else:
                start_vncserver(port)
        else:
            return 'vnc notfound'

def run_server(server_ip):
    app.server_ip = server_ip
    app.run(host='0.0.0.0', port=4584)
