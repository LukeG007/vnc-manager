from flask import Flask, request
import requests

app = Flask(__name__)

def auth(auth):
    r = requests.get()

@app.route('/start', methods=['POST'])
def start_vnc():
    data = dict(request.form)
    auth = data['auth']

def run_server():
    app.run(host='0.0.0.0', port=4584)
