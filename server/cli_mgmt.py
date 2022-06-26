import sqlite3
import auth_cli

class CLI:
    def __init__(self):
        self.auth = auth_cli.AuthenticationManagement()
        self.cmd_callbacks = {
            'help': {'usage': 'Display Command usages', 'callback': self.help},
            
        }
    def help(self):
        help_msg = ''
        for cmd in self.cmd_callbacks:
            usage = self.cmd_callbacks[cmd]['usage']
            help_msg += cmd + '\t' + usage + '\n'
        return help_msg
    def process_cmd(self, cmd, username, passwd):
        if self.auth.auth(username, passwd):
            self.cmd_callbacks[cmd]['callback']()
        else:
            return 'Invalid Credentials'
