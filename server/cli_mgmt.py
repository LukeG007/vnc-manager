import sqlite3
import auth_cli

class CLI:
    def __init__(self, extra_cmds=None):
        self.auth = auth_cli.AuthenticationManagement()
        self.cmd_callbacks = {
            'help': {'usage': 'help', 'desc': 'Display CMDs', 'callback': self.help, 'permission_required': 0, 'expected_arg_amount': 1},
            'user_details': {'usage': 'user_details <user>', 'desc': 'Get user info', 'callback': self.user_details, 'permission_required': 0, 'expected_arg_amount': 2}
        }
        if not extra_cmds is None:
            for cmd in extra_cmds:
                self.cmd_callbacks[cmd] = extra_cmds[cmd]
    def validate_cmd(self, args, amount_expected):
        return len(args) == amount_expected  
    def user_details(self, args):
        username = args[1]
        user, permissions, user_found = self.auth.get_user_details(username)
        if not user_found:
            return 'No user with that username was found'
        return 'Username: {}\nPermissions: {} ({})'.format(user, permissions, self.parse_permission_int(permissions))
    def help(self, args):
        help_msg = 'Command\tUsage\tDescription\tPermission Required\n'
        x = 1
        for cmd in self.cmd_callbacks:
            usage = self.cmd_callbacks[cmd]['usage']
            desc = self.cmd_callbacks[cmd]['desc']
            if not x == len(self.cmd_callbacks):
                help_msg += cmd + '\t' + usage + '\t' + desc + '\t' + self.parse_permission_int(self.cmd_callbacks[cmd]['permission_required']) + '\n'
            else:
                help_msg += cmd + '\t' + usage + '\t' + desc + '\t' + self.parse_permission_int(self.cmd_callbacks[cmd]['permission_required'])
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
        if not args[0] in self.cmd_callbacks:
            return 'Command not found'
        if not self.validate_cmd(args, self.cmd_callbacks[args[0]]['expected_arg_amount']):
            return 'Usage: ' + self.cmd_callbacks[args[0]]['usage']
        if auth and self.cmd_callbacks[args[0]]['permission_required'] <= permissions:
            return self.cmd_callbacks[args[0]]['callback'](args)
        else:
            return 'Invalid Credentials'
