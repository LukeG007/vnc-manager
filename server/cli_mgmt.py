import sqlite3
import auth_cli

class CLI:
    def __init__(self, extra_cmds=None):
        self.auth = auth_cli.AuthenticationManagement()
        self.cmd_callbacks = {
            'help': {'usage': 'Display CMDs', 'callback': self.help, 'permission_required': 0},
            'user_details': {'usage': 'Get user info', 'callback': self.user_details, 'permission_required': 0}
        }
        if not extra_cmds is None:
            for cmd in extra_cmds:
                self.cmd_callbacks[cmd] = extra_cmds[cmd]
    def user_details(self, args):
        username = args[1]
        user, permissions = self.auth.get_user_details(username)
        return 'Username: {}\nPermissions: {} ({})'.format(user, permissions, self.parse_permission_int(permissions))
    def help(self, args):
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
        auth = self.auth.auth(username, passwd)
        if not auth == False:
            permissions = auth
            auth = True
        args = cmd.split(' ')
        if auth and self.cmd_callbacks[args[0]]['permission_required'] <= permissions:
            return self.cmd_callbacks[args[0]]['callback'](args)
        else:
            return 'Invalid Credentials'
