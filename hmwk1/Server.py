import sys
import socket
import Common
from thread import *

configuration = Common.read_config()

class CreateServer(object):
    """
    Creates a server at IP and specifed port.
    """
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.userpasswd = Common.load_password(configuration['location']['passwdf'])
        server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            server.bind((host,port))
        except socket.error as e:
            print ("Binding failed. Error:%s",e)
            sys.exit()
        server.listen(10)
        print "Server Running"
        while 1:
            conn,addr = server.accept()
            print "Connected to ",addr
            self.client(conn)

    def client(self,conn):
        conn.send("Welcome to Simple Chat Server Please type your user name \n")
        conn.send("username:")
        username = conn.recv(1024)
        conn.send("password")
        password = conn.recv(1024)
a = CreateServer('127.0.0.1',8080)




