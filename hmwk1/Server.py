#! /usr/bin/python
import sys
import socket
import Common
import os
import threading
import time
import logging
logger = logging.getLogger()
FORMAT = "[%(levelname)s:%(threadName)-10s:%(funcName)20s] %(message)s" 
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.DEBUG)
consoleHandler = logging.StreamHandler()
logger.addHandler(consoleHandler)
configuration = Common.read_config()
userpasswd = Common.load_password(configuration['location']['passwdf'])
block_time = configuration['BLOCK_TIME']
numfailattempt = configuration['NUMFAILATT']
blocked_user = []
logged_user  = {}
auth_users = []
return_status = configuration["return_status"]

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
    time_run =1
    logging.info("Current Thread %s",threading.currentThread())
    while (time_run<=3):
        clientsocket.send("username:")
        username = clientsocket.recv(1024).strip()
        clientsocket.send("password:")
        password = clientsocket.recv(1024).strip()
        auth_status = authenticate(username,password)
        if auth_status ==0:
            time_run+=1
            break;
        if auth_status ==1:
            clientsocket.send("Welcome to Simple Chat Server\n")
            time_run = 4
            logged_user[time.time()] = username.strip()
            auth_users.append(username)
            c = Commands(clientsocket, username, auth_users)
            commands(clientsocket, username, c)
    
    if time_run ==3:
        clientsocket.close()
        blocked_user.append(username)
        
def authenticate(username, password):
    if username not in auth_users:
        password = password.strip()
        username = username.strip()
        reqpassword = userpasswd[username]
        reqpassword = reqpassword.strip()
        if reqpassword == password:
            logging.debug("Authentication for %s Successful",username)
            return 1
        else:
            logging.debug("Authentication for %s Unsuccessful",username)
            return 2
    else:
        logger.debug("User %s already logged in",username)
        return 2
def commands(clientsocket, username, c):
    running = True
    clientsocket.send("Type help for the list of commands available\n$")
    print "Execute"
    while running:
        clientsocket.send("$")
        input = clientsocket.recv(1024)
        input = input.strip()
        if input == "logout":
            c.logout()
            running = False
        if input == "whoelse":
            c.whoelse()


class Commands(object):
    """
    Commands supported for the Chat server.
    """
    def __init__(self,clientsocket,username,auth_users,**kwargs):
        self.clientsocket = clientsocket
        self.username = username
        self.auth_users = auth_users
    # def help(self):
        # for command in command_list:
            # self.clientsocket.send()
    def cleanup(self):
        self.auth_users.remove(self.username)
        self.clientsocket.close()
    def logout(self):
        self.cleanup()
    def whoelse(self):
        for values in auth_users:
            self.clientsocket.send(values)
    def wholast(self,time):
        pass
    def broadcast_message(self,message):
        pass
    def message(self,username):
        pass

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "Shutting Down Bye!!"
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)





