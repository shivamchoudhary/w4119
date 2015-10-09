#! /usr/bin/python
import sys
import socket
import Common
import os
import threading
import time
import logging
import userinfo

configuration           = Common.read_config()
userpass_dict,usernames = Common.load_password(configuration['location']['passwdf'])
block_time              = configuration['BLOCK_TIME']
numfailattempt          = configuration['NUMFAILATT']
return_status           = configuration["return_status"]
user_logintime = {}
loggedin_list =[] #list of users currently logged in the server
blocked_user = [] #list of users currently blocked in the server
blocked_ip = [] #list of IP's currently blocked in the server
blocked_sockets = [] #list of sockets currently blocked in the server
user_socket = {}
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
            print ("Socket binding failed with error %s", error)
            sys.exit(0)
        serversocket.listen(9)
        print ("Server Running")
        run = True
        while run:
            (clientsocket, clientaddress) = serversocket.accept()
            print ("Starting New Thread for IP:%s and socket %s",
                    clientaddress,clientsocket)
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
    print ("Current Thread %s", threading.currentThread())
    initial(clientsocket,clientaddr)

def initial(clientsocket,clientaddr):
    Common.send_msg(clientsocket, "username:")
    username = Common.recv_msg(clientsocket)
    Common.send_msg(clientsocket, "password:")
    password = Common.recv_msg(clientsocket)
    print 'Username:',username,'Password:',password
    newClient = userinfo.userInfo(username, password, clientsocket, clientaddr)
    authenticate(newClient)

def authenticate(newClient):
    if (newClient.username in usernames 
            and newClient.username not in loggedin_list 
            and newClient.username not in blocked_user
            and newClient.ip not in blocked_ip 
            and newClient.socket not in blocked_sockets):
        #password correct
        if newClient.password == userpass_dict[newClient.username]:
            newClient.login_attempt +=1
            Common.send_msg(newClient.socket,"1")
            loggedin_list.append(newClient.username)
            user_socket[newClient.username] = newClient.socket
            newClient.login_time = int(round(time.time()*1000))
            user_logintime[newClient.username] = newClient.login_time
            parse_a_command(newClient)
        #password incorrect attempt
        else:
            newClient.login_attempt +=1
            #Maximum retries reached closing the connection
            if newClient.login_attempt >=numfailattempt:
                Common.send_msg(newClient.socket,"5")
                blocked_user.append(newClient.username)
                blocked_ip.append(newClient.ip)
                print "Maximum retries reached !!",blocked_user,blocked_ip
            #Maximum retries not reached try again!
            else:
                Common.send_msg(newClient.socket,"6")
                retry_authentication(newClient)
    #username not present or user already logged in!!
    else:
        Common.send_msg(newClient.socket,"4")
        newClient.socket.close()
        return False
def parse_a_command(newClient):
    input  = True
    while input:
        try:
            input = Common.recv_msg(newClient.socket)
            command = input.split(" ")
            print command
            if command[0] =="whoelse":
                output = []
                for users in loggedin_list: 
                    output.append(users)
                Common.send_msg(newClient.socket,",".join(output))

            elif command[0] =="wholast":
                output = []
                try:
                    limit = int(command[1])
                    cur_time = int(round(time.time()*1000))
                    for k,v in user_logintime.iteritems():
                        if v-cur_time<limit:
                            output.append(k)
                    result = "".join(output)
                    result = str(result)
                    
                    Common.send_msg(newClient.socket,result)
                except IndexError:
                    Common.send_msg(newClient.socket,"7")
            elif command[0]=="message":
                try:
                    username = command[1]
                    message = command[2:]
                    output = []
                    for k,v in user_socket.iteritems():
                        if k==username:
                            message = ",".join(message)
                            Common.send_msg(v,message)
                    Common.send_msg(newClient.socket,"10")

                except IndexError:
                    Common.send_msg(newClient.socket,"7")
            elif command[0]=="logout":
                loggedin_list.remove(newClient.username)
                del(user_logintime[newClient.username])
                Common.send_msg(newClient.socket,"8")
                newClient.socket.close()
                break
            elif command[0]=="broadcast" and command[1]=="message":
                try:
                    message = command[2:]
                    message = "".join(message)
                    for k,v in user_socket.iteritems():
                        Common.send_msg(v,message)
                except IndexError:
                    Common.send_msg(newClient.socket,"7")
            elif command[0]=="broadcast" and command[1]=="user":
                try:
                    index = command.index("message")
                    user_list = command[2:index]
                    message = command[index:]
                    message = "".join(message)
                    for k,v in user_socket.iteritems():
                        if k in user_list:
                            Common.send_msg(v,message)
                except IndexError:
                    Common.send_msg(newClient.socket,"7")
            #command not recognized be server send 9.
            else:
                Common.send_msg(newClient.socket,"9")
        except Exception as e:
            newClient.socket.close()
            print 'Caught an exception',e
            break
def retry_authentication(newClient):
    Common.send_msg(newClient.socket,"password:")
    newClient.password = Common.recv_msg(newClient.socket)
    authenticate(newClient)
def timer(username,clientsocket):
    print 'Spawning new thread',threading.currentThread()
    time.sleep(block_time)
    blocked_user.remove(username)
    blocked_socket.remove(clientsocket)
    client_loginattempt[username] = 0
    print 'Removing user',blocked_user 
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "Shutting Down the Server Bye!!"
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

