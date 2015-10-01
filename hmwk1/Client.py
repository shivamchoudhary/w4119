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

    def __init__(self, serversocket):
        self.serversocket = serversocket
        init_run = True
        while init_run:
            sys.stdout.write(Common.recv_msg(self.serversocket))
            username = raw_input()
            Common.send_msg(self.serversocket, username)
            sys.stdout.write(Common.recv_msg(self.serversocket))
            password = raw_input()
            Common.send_msg(self.serversocket,password)
            init_run = False
            self.auth_status = Common.recv_msg(self.serversocket)
            print self.auth_status
    

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
