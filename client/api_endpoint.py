from flask import Flask

app = Flask(__name__)

def run_server():
    app.run(host='0.0.0.0', port=4584)
