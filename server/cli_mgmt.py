import sqlite3
import auth_cli

class CLI:
    def __init__(self):
        self.auth = auth_cli.AuthenticationManagement()
        self.cmd_callbacks = {
            'help': {'usage': 'Display Command Details', 'callback': self.help},
            
        }
    def help(self):
        help_msg = 'Command\tDescription\n'
        x = 1
        for cmd in self.cmd_callbacks:
            usage = self.cmd_callbacks[cmd]['usage']
            if not x == len(self.cmd_callbacks):
                help_msg += cmd + '\t' + usage + '\n'
            else:
                help_msg += cmd + '\t' + usage
            x += 1
        return help_msg
    def process_cmd(self, cmd, username, passwd):
        if self.auth.auth(username, passwd):
            return self.cmd_callbacks[cmd]['callback']()
        else:
            return 'Invalid Credentials'
