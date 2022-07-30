import cli_mgmt
from tabulate import tabulate
import sqlite3

class CLISessionManagement:
    def __init__(self, username, password, vnc_sys, client_sys, ste=None):
        extra_cmds={
            'whoami': {'usage': 'whoami', 'desc': 'Check current user', 'callback': self.whoami, 'permission_required': 0, 'expected_arg_amount': 1},
            'list_vncs': {'usage': 'list_vncs', 'desc': 'List all vnc servers', 'callback': self.list_vncs, 'permission_required': 0, 'expected_arg_amount': 1},
            'list_hosters': {'usage': 'list_hosters', 'desc': 'List all machines that host VNC servers', 'callback': self.list_hosters, 'permission_required': 0, 'expected_arg_amount': 1},
            'create_vnc': {'usage': 'create_vnc <port>', 'desc': 'Create vnc server', 'callback': self.create_vnc, 'permission_required': 2, 'expected_arg_amount': 2},
            'delete_vnc': {'usage': 'delete_vnc <port>', 'desc': 'Delete vnc server', 'callback': self.delete_vnc, 'permission_required': 2, 'expected_arg_amount': 2},
            'create_user': {'usage': 'create_user <username> <password> <permission>', 'desc': 'Creates User', 'callback': self.create_user, 'permission_required': 2, 'expected_arg_amount': 4},
            'delete_user': {'usage': 'delete_user <username>', 'desc': 'Deletes User', 'callback': self.delete_user, 'permission_required': 2, 'expected_arg_amount': 2},
            'start_vnc': {'usage': 'start_vnc <port>', 'desc': 'Start vnc server', 'callback': self.start_vnc, 'permission_required': 1, 'expected_arg_amount': 2},
            'stop_vnc': {'usage': 'stop_vnc <port>', 'desc': 'Stop vnc server', 'callback': self.stop_vnc, 'permission_required': 1, 'expected_arg_amount': 2},
        }
        self.cli = cli_mgmt.CLI(vnc_sys, extra_cmds=extra_cmds)
        self.username = username
        self.vnc_sys = vnc_sys
        self.client_sys = client_sys
        self.password = password
        self.ste = ste
    def whoami(self, args):
        return self.cli.user_details([None, self.username])
    def list_vncs(self, args):
        tab_headers = ['Owner', 'Port', 'Server']
        db = sqlite3.connect(self.vnc_sys.db_name)
        cur = db.cursor()
        cur.execute('SELECT username, port, server FROM vnc_servers')
        data = cur.fetchall()
        cur.close()
        db.close()
        message = tabulate(data, headers=tab_headers)
        return message
    def create_user(self, args):
        author, author_permissions, user_found = self.cli.auth.get_user_details(self.username)
        permissions = int(args[3])
        if permissions <= author_permissions:
            self.cli.auth.add_user(args[1], args[2], permissions)
            return 'ok'
        return 'noauth'
    def delete_user(self, args):
        self.cli.auth.delete_user(args[1])
        return 'ok'
    def list_hosters(self, args):
        tab_headers = ['Hostname', 'IP', 'MGMT ID', 'Load', 'Online']
        db = sqlite3.connect(self.client_sys.db)
        cur = db.cursor()
        cur.execute('SELECT * FROM clients')
        data = cur.fetchall()
        cur.close()
        db.close()
        online_client_list = self.client_sys.client_list
        tab_data = []
        for client in data:
            online = client[0] in online_client_list
            hostname = client[1]
            ip = client[2]
            load = client[3]
            tab_data.append([hostname, ip, client[0], load, online])
        message = tabulate(tab_data, headers=tab_headers)
        return message

    def create_vnc(self, args):
        port = args[1]
        resp = self.vnc_sys.create_vnc_server(self.username, self.password, port)
        if resp[1] == 1:
            resp = 'ERROR: '+resp[0]
        else:
            resp = resp[0]
        return resp
    def delete_vnc(self, args):
        port = args[1]
        resp = self.vnc_sys.delete_vnc_server(self.username, self.password, port)
        if resp[1] == 1:
            resp = 'ERROR: '+resp[0]
        else:
            resp = resp[0]
        return resp
    def start_vnc(self, args):
        port = args[1]
        resp = self.vnc_sys.start_vnc_server(port, self.username, self.password)
        if resp[1] == 1:
            resp = 'ERROR: '+resp[0]
        else:
            resp = resp[0]
        return resp
    def stop_vnc(self, args):
        port = args[1]
        resp = self.vnc_sys.stop_vnc_server(port, self.username, self.password)
        if resp[1] == 1:
            resp = 'ERROR: '+resp[0]
        else:
            resp = resp[0]
        return resp
    def execute(self, cmd):
        return self.cli.process_cmd(cmd, self.username, self.password)
