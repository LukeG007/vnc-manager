import cli_mgmt

class CLISessionManagement:
    def __init__(self, username, password, vnc_sys, ste=None):
        extra_cmds={
            'whoami': {'usage': 'whoami', 'desc': 'Check current user', 'callback': self.whoami, 'permission_required': 0, 'expected_arg_amount': 1},
            'create_vnc': {'usage': 'create_vnc <port>', 'desc': 'Create vnc server', 'callback': self.create_vnc, 'permission_required': 2, 'expected_arg_amount': 2},
            'start_vnc': {'usage': 'start_vnc <port>', 'desc': 'Start vnc server', 'callback': self.start_vnc, 'permission_required': 1, 'expected_arg_amount': 2},
            'stop_vnc': {'usage': 'stop_vnc <port>', 'desc': 'Stop vnc server', 'callback': self.stop_vnc, 'permission_required': 1, 'expected_arg_amount': 2}
        }
        self.cli = cli_mgmt.CLI(vnc_sys, extra_cmds=extra_cmds)
        self.username = username
        self.vnc_sys = vnc_sys
        self.password = password
        self.ste = ste
    def whoami(self, args):
        return self.cli.user_details([None, self.username])
    def create_vnc(self, args):
        port = args[1]
        resp = self.vnc_sys.create_vnc_server(self.username, self.password, port)
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
