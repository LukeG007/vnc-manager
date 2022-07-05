import sqlite3

class VNCManagement:
    def __init__(self, auth, client_sys):
        self.db_name = 'data.sqlite'
        self.db = sqlite3.connect(self.db_name)
        self.auth = auth
        self.client_sys = client_sys
        cur = self.db.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS vnc_servers(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, port INTEGER, server TEXT)')
        cur.close()
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
                            if lowest_load_server['vnc_server_amount'] > client['vnc_server_amount']:
                                lowest_load_server = client
                    server = lowest_load_server['vnc_server_amount']
                
                cur.execute('INSERT INTO vnc_servers VALUES(null, "{}", "{}", "{}")'.format(username, port, server))
                cur.close()
            else:
                cur.close()
                return 'AUTH_FAILED'
        else:
            return 'VNC_EXISTS'
