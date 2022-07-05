import uuid

class ClientManagement:
    def __init__(self):
        self.client_list = {}
    def add_client(self, hostname, ip):
        mgmt_id = str(uuid.uuid4()).split('-')[0]
        self.client_list[ip] = {'hostname': hostname, 'mgmt_id': mgmt_id, 'vnc_server_amount': 0}
