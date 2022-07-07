import uuid
import requests

class ClientManagement:
    def __init__(self):
        self.client_list = {}
    def add_client(self, hostname, ip):
        mgmt_id = str(uuid.uuid4()).split('-')[0]
        self.client_list[mgmt_id] = {'hostname': hostname, 'ip': ip, 'vnc_server_amount': 0}
    def send_start_cmd(self, mgmt_id, authentication, port):
        server = self.client_list[mgmt_id]
        requests.post('http://{}:4584/start'.format(server['ip']), json={'auth': authentication, 'port': port})
