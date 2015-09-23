#! /usr/bin/python
import sys
import socket
import Common
import thread
import os
import threading
import time

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
            print ("Binding failed. Error:%s",error)
            sys.exit(0)
        serversocket.listen(5)
        print "Server Running"
        while True:
            (clientsocket, clientaddress)  = serversocket.accept()
            print auth_users
            thread.start_new_thread(handlerequests, 
                    (clientsocket, clientaddress))


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
        username = clientsocket.recv(1024).strip()
        clientsocket.send("password:")
        password = clientsocket.recv(1024).strip()
        if authenticate(username,password):
            clientsocket.send("Welcome to Simple Chat Server\n")
            run = False
            logged_user[time.time()] = username.strip()
            auth_users.append(username)
            c = Commands(clientsocket,username,auth_users)
            commands(clientsocket,username,c)

def authenticate(username,password):
    if username not in auth_users:
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
    else:
        print "user already logged in"
        return 2
def commands(clientsocket,username,c):
    clientsocket.send("Type help for the list of commands available\n$")
    input = clientsocket.recv(1024)
    input = input.strip()
    if input =="logout":
        c.logout()
    if input =="whoelse":
        c.whoelse()


class Commands(object):
    def __init__(self,clientsocket,username,auth_users,**kwargs):
        self.clientsocket = clientsocket
        self.username = username
        self.auth_users = auth_users
    def cleanup(self):
        self.auth_users.remove(self.username)
        self.clientsocket.close()
    def logout(self):
        self.cleanup()
    def whoelse(self):
        for values in auth_users:
            self.clientsocket.send(values)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "Shutting Down Bye!!"
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)





