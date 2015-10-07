import sys
import os
import socket
import Common
configuration = Common.read_config()
stat_message = configuration["return_status"]

def connect(ip, port):
    """
    Used the Python Socket API to create the TCP/IP Socket
    https://docs.python.org/2/library/socket.html
    """
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
        auth_status = self.authenticate(self.serversocket,auth_status = True)
        
        if int(auth_status) == 1:
            sys.stdout.write(Common.recv_msg(self.serversocket))
            self.input(self.serversocket)

    def authenticate(self, socket, auth_status):
        while auth_status:
            sys.stdout.write(Common.recv_msg(self.serversocket))
            username = raw_input()
            Common.send_msg(self.serversocket,username)
            sys.stdout.write(Common.recv_msg(self.serversocket))
            password = raw_input()
            Common.send_msg(self.serversocket,password)
            auth_status = False
        return Common.recv_msg(self.serversocket)
    
    def input(self,socket):
        while True:
            sys.stdout.write("$")
            command = raw_input()
            if command:
                Common.send_msg(socket,command)
            else:
                Common.recv_msg(socket)
                while True:
                    data = Common.recv_msg(socket)
                    if data != str(2) and data:
                        print data
                    else:
                        break

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
