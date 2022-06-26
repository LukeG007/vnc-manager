import hashlib
import sqlite3
import os

class AuthenticationManagement:
    def __init__(self):
        self.db_name = 'auth.sqlite'
        self.db = sqlite3.connect(self.db_name)
        cur = self.db.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, key TEXT)')
        cur.close()
    def auth(self, username, passwd):
        cur = self.db.cursor()
        cur.execute('SELECT * FROM users')
        users = cur.fetchall()
        cur.close()
        authenticated = False
        for user in users:
            if user[1] == username:
                salt = user[2][:32]
                key = user[2][32:]
                new_key = hashlib.pbkdf2_hmac(
                    'sha256',
                    passwd.encode('utf-8'),
                    salt,
                    100000
                )
                if new_key == key:
                    authenticated = True
        return authenticated
    def add_user(self, username, passwd):
        cur = self.db.cursor()
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac(
            'sha256',
            passwd.encode('utf-8'),
            salt,
            100000
        )
        hashed_passwd = salt + key
        cur.execute('INSERT INTO users VALUES(null, "{}", "{}")'.format(username, hashed_passwd))
