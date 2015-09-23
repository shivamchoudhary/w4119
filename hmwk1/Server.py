#! /usr/bin/python
import sys
import socket
import Common
import thread
import os
import threading

configuration = Common.read_config()
userpasswd = Common.load_password(configuration['location']['passwdf'])
block_time = configuration['BLOCK_TIME']
numfailattempt = configuration['NUMFAILATT']
blocked_user = []
class CreateServer(object):
    """
    Creates a server on localhost at specifed port.
    """
    def __init__(self, port):
        """
        host can be specified in config.json file
        """
        self.host = configuration['host']
        self.port = port
        self.userpasswd = Common.load_password(
                configuration['location']['passwdf'])
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            serversocket.bind((self.host, self.port))
        except socket.error as error:
            print ("Binding failed. Error:%s",error)
            sys.exit(0)
        serversocket.listen(5)
        while True:
            (clientsocket, clientaddress)  = serversocket.accept()
            print "Socket %s Address %s", clientsocket, clientaddress
            thread.start_new_thread(handlerequests, 
                    (clientsocket, clientaddress))
        print "Server Running"


def main():
    """
    Main function creates a server on the specified port and handles
    KeyboardInterrupt.
    """
    try:
        port = int(sys.argv[1])
    except IndexError:
        print "Please specify a port number to bind the server."
        sys.exit()
    CreateServer(port)

def handlerequests(clientsocket, clientaddr):
    run = True
    while run:
        clientsocket.send("username:")
        username = clientsocket.recv(1024)
        clientsocket.send("password:")
        password = clientsocket.recv(1024)
        if authenticate(username,password):
            clientsocket.send("Welcome to the Chat Server\n")
            run = False
            commands(clientsocket)
        else:
            clientsocket.send("**Authentication Failed**\n")
            clientsocket.send("password:")
    clientsocket.close()



def authenticate(username,password):
    password = password.strip()
    username = username.strip()
    reqpassword = userpasswd[username]
    reqpassword = reqpassword.strip()
    if reqpassword == password:
        print "Authentication Successful"
        return True
    else:
        print "Authentication Unsuccessful"
        return False
def commands(clientsocket):
    clientsocket.send("Type help for the list of commands available\n$")
    input = clientsocket.recv(1024)
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "Shutting Down Bye!!"
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)





