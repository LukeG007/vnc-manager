import hashlib
import sqlite3
import os
import codecs

class AuthenticationManagement:
    def __init__(self):
        self.db_name = 'auth.sqlite'
        self.db = sqlite3.connect(self.db_name)
        cur = self.db.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, key TEXT, permissions INTEGER)')
        cur.close()
    def auth(self, username, passwd):
        cur = self.db.cursor()
        cur.execute('SELECT * FROM users')
        users = cur.fetchall()
        cur.close()
        authenticated = False
        for user in users:
            if user[1] == username:
                hex_decoded = codecs.decode(user[2], 'hex_codec')
                salt = hex_decoded[:32]
                key = hex_decoded[32:]
                new_key = hashlib.pbkdf2_hmac(
                    'sha256',
                    passwd.encode('utf-8'),
                    salt,
                    100000
                )
                if new_key == key:
                    authenticated = True
        return authenticated, user[2]
    def get_user_details(self, username):
        cur = self.db.cursor()
        cur.execute('SELECT * FROM users')
        users = cur.fetchall()
        cur.close()
        permissions = 0
        for user in users:
            if user[1] == username:
                permissions = user[2]
        return username, permissions
    def add_user(self, username, passwd, permissions):
        cur = self.db.cursor()
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac(
            'sha256',
            passwd.encode('utf-8'),
            salt,
            100000
        )
        hashed_passwd = codecs.encode(salt + key, 'hex_codec').decode('utf-8')
        cur.execute('INSERT INTO users VALUES(null, "{}", "{}", {})'.format(username, hashed_passwd, permissions))
        cur.close()
        self.db.commit()
