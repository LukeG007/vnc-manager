import cli_mgmt

class CLISessionManagement:
    def __init__(self, username, password):
        self.cli = cli_mgmt.CLI(extra_cmds={
            'whoami': {'usage': 'Check current user', 'callback': self.whoami, 'permission_required': 0, 'expected_arg_amount': 1}
        })
        self.username = username
        self.password = password
    def whoami(self, args):
        return self.cli.user_details([None, self.username])
    def execute(self, cmd):
        return self.cli.process_cmd(cmd, self.username, self.password)
