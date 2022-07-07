import cli_mgmt

class CLISessionManagement:
    def __init__(self, username, password, vnc_sys):
        self.cli = cli_mgmt.CLI(vnc_sys, extra_cmds={
            'whoami': {'usage': 'whoami', 'desc': 'Check current user', 'callback': self.whoami, 'permission_required': 0, 'expected_arg_amount': 1},
            'create_vnc': {'usage': 'create_vnc <port>', 'desc': 'Create vnc server', 'callback': self.create_vnc, 'permission_required': 2, 'expected_arg_amount': 3},
            'start_vnc': {'usage': 'start_vnc <port>', 'desc': 'Start vnc server', 'callback': self.start_vnc, 'permission_required': 1, 'expected_arg_amount': 2}
        })
        self.username = username
        self.password = password
    def whoami(self, args):
        return self.cli.user_details([None, self.username])
    def create_vnc(self, args):
        port = args[1]
        self.cli.vnc_sys.create_vnc_server(self.username, self.password, port)
    def start_vnc(self, args):
        port = args[1]
        self.vnc_sys.start_vnc_server(port, self.username, self.password)
    def execute(self, cmd):
        return self.cli.process_cmd(cmd, self.username, self.password)
