import sqlite3
import os
import json

class VNCManagement:
    def __init__(self, auth):
        self.db_name = 'data.sqlite'
        self.db = sqlite3.connect(self.db_name)
        self.auth = auth
        cur = self.db.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS vnc_servers(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, port INTEGER)')
        cur.close()
    def create_vnc_server(self, username, passwd, port):
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
                cur.execute('INSERT INTO vnc_servers VALUES(null, "{}", "{}")'.format(username, port))
                cur.close()
            else:
                cur.close()
                return 'AUTH_FAILED'
        else:
            return 'VNC_EXISTS'
