import sqlite3
import requests

class VNCManagement:
    def __init__(self, auth, client_sys):
        self.db_name = 'data.sqlite'
        self.db = sqlite3.connect(self.db_name)
        self.auth = auth
        self.client_sys = client_sys
        cur = self.db.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS vnc_servers(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, port INTEGER, server TEXT)')
        cur.close()
    def start_vnc_server(self, port, username, passwd):
        authenticated = self.auth.auth(username, passwd)
        if not authenticated == False:
            permissions = authenticated
            cur = self.db.cursor()
            try:
                cur.execute('SELECT * FROM vnc_servers WHERE port={}'.format(port))
            except sqlite3.Error:
                cur.close()
                return ['notfound', 1]
            server_entry = cur.fetchall()[0]
            if not server_entry[1] == username and permissions == 0:
                cur.close()
                return ['unprivileged', 1]
            cur.close()
            self.client_sys.send_start_cmd(server_entry[3], username+':'+passwd, port)
            return ['ok', 0]
        else:
            cur.close()
            return ['noauth', 1]
    def get_vnc_data(self):
        cur = self.db.cursor()
        cur.execute('SELECT username, port, server FROM vnc_servers')
        data = cur.fetchall()
        vnc_data = {}
        for entry in data:
            entry_data = {}
            entry_data['username'] = entry[0]
            entry_data['server'] = entry[2]
            vnc_data[entry[1]] = entry_data
        
        return vnc_data

    def create_vnc_server(self, username, passwd, port, server=None):
        cur = self.db.cursor()
        cur.execute('SELECT * FROM vnc_servers')
        vnc_servers = cur.fetchall()
        vnc_exists = False
        for vnc in vnc_servers:
            if vnc['username'] == username and vnc['port'] == port:
                vnc_exists = True
        if not vnc_exists:
            authenticated = self.auth.auth(username, passwd)
            if not authenticated == False:
                if server is None:
                    server_load = {}
                    for client in self.client_sys.client_list:
                        server_load[client['mgmt_id']] = client['vnc_server_amount']
                    lowest_load_server = None
                    for client in self.client_sys.client_list:
                        if lowest_load_server == None:
                            lowest_load_server = client
                        else:
                            if self.client_sys.client_list[lowest_load_server['vnc_server_amount']] > self.client_sys.client_list[client['vnc_server_amount']]:
                                lowest_load_server = client
                    server = lowest_load_server
                
                cur.execute('INSERT INTO vnc_servers VALUES(null, "{}", "{}", "{}")'.format(username, port, server))
                cur.close()
                return ['ok', 0]
            else:
                cur.close()
                return ['noauth', 1]
        else:
            return ['exists', 1]
