import sqlite3
import auth_cli

class CLI:
    def __init__(self):
        self.auth = auth_cli.AuthenticationManagement()
        self.cmd_callbacks = {
            'help': {'usage': 'Display CMDs', 'callback': self.help, 'permission_required': 0}
        }
    def help(self):
        help_msg = 'Command\tDescription\tPermission Required\n'
        x = 1
        for cmd in self.cmd_callbacks:
            usage = self.cmd_callbacks[cmd]['usage']
            if not x == len(self.cmd_callbacks):
                help_msg += cmd + '\t' + usage + '\t' + self.parse_permission_int(self.cmd_callbacks[cmd]['permission_required']) + '\n'
            else:
                help_msg += cmd + '\t' + usage + '\t' + self.parse_permission_int(self.cmd_callbacks[cmd]['permission_required'])
            x += 1
        return help_msg
    def parse_permission_int(self, permission):
        if permission == 0:
            return 'Everyone'
        if permission == 1:
            return 'Mod'
        if permission == 2:
            return 'Admin'
        if permission == 3:
            return 'Owner'
    def process_cmd(self, cmd, username, passwd):
        auth, permission = self.auth.auth(username, passwd)
        if auth and self.cmd_callbacks[cmd]['permission_required'] <= permission:
            return self.cmd_callbacks[cmd]['callback']()
        else:
            return 'Invalid Credentials'
