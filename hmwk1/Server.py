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
user2socket             = {}
user_clientmap          = {}
return_status           = configuration["return_status"]

class CreateServer(object):
    """
    Creates a server on localhost at specifed port.
    Citatations:-
    Used the Python Socket API to create the TCP/IP Socket
    https://docs.python.org/2/library/socket.html
    Used the Python Threading API to spawn a new thread for handling the 
    different connections.
    https://docs.python.org/2/library/thread.html
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
        serversocket.listen(9)
        logger.debug("Server Running")
        run = True
        while run:
            (clientsocket, clientaddress) = serversocket.accept()
            logger.info("Starting New Thread for IP:%s and socket %s",
                    clientaddress, clientsocket)
            thread = threading.Thread(target=handlerequests, 
                    args=(clientsocket, clientaddress))
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
    username = username.strip()
    Common.send_msg(clientsocket,"password:")
    password = Common.recv_msg(clientsocket)
    password = password.strip()
    try:
        userpass_dict[username]       
        if password != userpass_dict[username]:
            Common.send_msg(clientsocket, "0")
        if password == userpass_dict[username]:
            auth_users.append(username)
            logged_user[username] = int(round(time.time())*1000)
            user2socket[clientsocket] = username
            Common.send_msg(clientsocket, "1")
            Common.send_msg(clientsocket,"Welcome to Chat Server!!\n")
            logging.debug("Login List %s and Auth user is %s",
                    auth_users, logged_user)
            command = Common.recv_msg(clientsocket)
            parse_a_command(clientsocket,command)
        if username in logged_user:
            Common.send_msg(clientsocket, "2")
        if username in blocked_user:
            Common.send_msg(clientsocket, "3")
    except KeyError:
        Common.send_msg(clientsocket,"4")

def parse_a_command(clientsocket,command):
    command = command.split(" ")
    if command[0] == "whoelse":
        for user in auth_users:
            Common.send_msg(clientsocket,user)
        return
    elif command[0] == "wholast":
        limit = int(command[1])
        cur_time = int(round(time.time()*1000))
        for k,v in logged_user.iteritems():
            if v-cur_time <limit:
                Common.send_msg(clientsocket,k)
    elif command[0] == "broadcast" and command[1]=="message":
        for k,v in user2socket.iteritems():
            Common.send_msg(k,command[2])
            print v,command[2]
    elif command[0] == "broadcast" and command[1]=="user":
        list_user = command[2:-1]
        for k,v in user2socket.iteritems():
            if v in list_user:
                print k,command[-1]
    elif command[0] == "message":
        user = command[1]
        print user,'USER'
        for k,v in user2socket.iteritems():
            print k,v
            if v ==user:
                print user,command[2:]
    elif command[0] =="logout":
        return 1
    return
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "Shutting Down the Server Bye!!"
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

