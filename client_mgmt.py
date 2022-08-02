import uuid
import requests
import sqlite3

class ClientManagement:
    def __init__(self):
        self.db = 'data.sqlite'
        db = sqlite3.connect(self.db)
        cur = db.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS clients(mgmt_id TEXT, hostname TEXT, ip TEXT, vnc_server_amount INTEGER)')
        cur.close()
        db.commit()
        db.close()
        self.client_list = {}

    def add_client(self, hostname, ip):
        self.ping_hosters()
        db = sqlite3.connect(self.db)
        cur = db.cursor()
        cur.execute('SELECT * FROM clients')
        clients = cur.fetchall()
        current_client = None
        for client in clients:
            if client[1] == hostname and client[2] == ip:
                current_client = client
        if not current_client == None:
            self.client_list[current_client[0]] = {'hostname': hostname, 'ip': ip, 'vnc_server_amount': current_client[3]}
            cur.close()
            db.close()
        else:
            mgmt_id = str(uuid.uuid4()).split('-')[0]
            self.client_list[mgmt_id] = {'hostname': hostname, 'ip': ip, 'vnc_server_amount': 0}
            cur.execute('INSERT INTO clients VALUES("{}", "{}", "{}", {})'.format(mgmt_id, hostname, ip, 0))
            cur.close()
            db.commit()
            db.close()
        return 'ok'
    def ping_hosters(self):
        db = sqlite3.connect(self.db)
        cur = db.cursor()
        cur.execute('SELECT mgmt_id, ip FROM clients')
        data = cur.fetchall()
        cur.close()
        for hoster in data:
            try:
                requests.get('http://{}:4584/ping'.format(hoster[1]))
            except:
                online = False
            else:
                online = True
            if not online and hoster[0] in self.client_list:
                del self.client_list[hoster[0]]
    def send_start_cmd(self, mgmt_id, authentication, port):
        self.ping_hosters()
        if not mgmt_id in self.client_list:
            return 'hoster offline'
        server = self.client_list[mgmt_id]
        requests.post('http://{}:4584/start'.format(server['ip']), data={'auth': authentication, 'port': port})
        return 'ok'
    def send_stop_cmd(self, mgmt_id, authentication, port):
        self.ping_hosters()
        if not mgmt_id in self.client_list:
            return 'hoster offline'
        server = self.client_list[mgmt_id]
        requests.post('http://{}:4584/stop'.format(server['ip']), data={'auth': authentication, 'port': port})
        return 'ok'
