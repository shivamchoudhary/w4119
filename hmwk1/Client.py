import sys
import os
import socket
import Common

configuration = Common.read_config()
stat_message = configuration["return_status"]

def connect(ip, port):
    try:
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (ip, port)
        serversocket.connect(server_address)
        Client(serversocket)
    except Exception as error:
        print "Caught Exception as %s", error


class Client(object):
    
    def __init__(self,serversocket):
        self.user_passwordstr= login()
        self.serversocket = serversocket
        self.authenticate(self.user_passwordstr)
    
    def authenticate(self,username_passwdstr):
        self.serversocket.send(self.user_passwordstr)


def login(**kwargs):
    username = raw_input("username:")
    password = raw_input("password:")
    user_passwdstr = username+"+"+password
    return user_passwdstr


def main():
    try:
        ip = sys.argv[1]
        port = int(sys.argv[2])
    except IndexError:
        print "Please specify <server IP_address> <server_port_no>"
    connect(ip, port)
    
if __name__=="__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "Shutting Down the client!!"
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
