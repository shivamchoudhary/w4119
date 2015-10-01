#! /usr/bin/python
import sys
import socket
import Common
import os
import threading
import time
import logging
logger                  = logging.getLogger()
FORMAT                  = "[%(levelname)s:%(threadName)-10s] %(message)s" 
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.DEBUG)
consoleHandler          = logging.StreamHandler()
logger.addHandler(consoleHandler)
configuration           = Common.read_config()
userpass_dict,usernames = Common.load_password(configuration['location']['passwdf'])
block_time              = configuration['BLOCK_TIME']
numfailattempt          = configuration['NUMFAILATT']
blocked_user            = []
logged_user             = {}
auth_users              = []
client_sockets          =[]
user_clientmap          = {}
return_status           = configuration["return_status"]

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
        serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        try:
            serversocket.bind((self.host, self.port))
        except socket.error as error:
            logging.critical("Socket binding failed with error %s", error)
            sys.exit(0)
        serversocket.listen(5)
        logger.debug("Server Running")
        while True:
            (clientsocket, clientaddress) = serversocket.accept()
            logger.info("Starting New Thread for IP:%s and socket %s",
                    clientaddress, clientsocket)
            thread = threading.Thread(target=handlerequests, args=(clientsocket,
                clientaddress))
            thread.deamon = True
            thread.start()

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
    """
    Threading for handling requests.
    """
    run = True
    logging.info("Current Thread %s", threading.currentThread())
    authenticate(clientsocket)
           
def authenticate(clientsocket):
    Common.send_msg(clientsocket,"username:")
    username = Common.recv_msg(clientsocket)
    Common.send_msg(clientsocket,"password:")
    password = Common.recv_msg(clientsocket)
    try:
        userpass_dict[username]
        if password != userpass_dict[username]:
            Common.send_msg(clientsocket, "0")
        if password == userpass_dict[username]:
            Common.send_msg(clientsocket, "1")
        if username in logged_user:
            Common.send_msg(clientsocket, "2")
        if username in blocked_user:
            Common.send_msg(clientsocket, "3")
    except KeyError:
        Common.send_msg(clientsocket,"4")


def commands(clientsocket, username, c):
    running = True
    clientsocket.send("Type help for the list of commands available\n")
    while running:
        clientsocket.send("$")
        input = clientsocket.recv(1024)
        input = input.strip()
        input = input.split()
        if input[0] == "logout":
            c.logout()
            running = False
        if input[0] == "whoelse":
            c.whoelse()
        if input[0] == "broadcast" and input[1] == "message":
            c.broadcast_message(input[1])
        if input[0] == "message":
            reciever = input[1]
            message = input[2]
            c.message(reciever,message,username)

class Commands(object):
    """
    Commands supported for the Chat server.
    """
    def __init__(self, clientsocket, username, auth_users, **kwargs):
        self.clientsocket = clientsocket
        self.username = username
        self.auth_users = auth_users
    
    def cleanup(self):
        self.auth_users.remove(self.username)
        self.clientsocket.close()
    
    def logout(self):
        logger.debug("USER:%s is logging out",self.username)
        self.cleanup()
    
    def whoelse(self):
        for values in auth_users:
            self.clientsocket.send(values)
            self.clientsocket.send("\n")
    
    def wholast(self, time):
        pass
    
    def broadcast_message(self,message):
        for client in client_sockets:
            client.send(message)
    
    def message(self,reciever,message,sender):
        reciever_clientsocket = user_clientmap[reciever]
        message = sender+":"+message
        reciever_clientsocket.send(message)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "Shutting Down Bye!!"
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)





