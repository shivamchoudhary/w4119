import time
import socket
class userInfo:

    def __init__(self, username, password,socket,address):
        self.username = username
        self.password = password
        self.login_attempt = 0
        self.login_time = time.time()
        self.socket = socket
        self.ip  =address[0]
        self.port = address[1]
        self.admin = False
    def wrong_passwd(self):
        self.login_attempt += 1

