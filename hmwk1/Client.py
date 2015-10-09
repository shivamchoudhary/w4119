import sys
import os
import socket
import Common
import select
import threading
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
        # serversocket.settimeout(0.5)
        Client(serversocket)
    except Exception as error:
        print "Caught Exception as %s", error
        serversocket.close()
        
class Client(object):

    def __init__(self, serversocket):
        self.serversocket = serversocket
        self.authenticate() 
    def authenticate(self):
        try:
            sys.stdout.write(Common.recv_msg(self.serversocket))
            username = raw_input()
            Common.send_msg(self.serversocket,username)
            sys.stdout.write(Common.recv_msg(self.serversocket))
            password = raw_input()
            Common.send_msg(self.serversocket,password)
            auth_status = Common.recv_msg(self.serversocket)
            if auth_status ==str(4):
                print "User does not exist or is already logged/in blocked list"
                "Closing the connection"
                self.serversocket.close()
                sys.exit(0)
            elif auth_status ==str(1):
                print "Welcome to Chat Server!!"
                self.commands()
            elif auth_status ==str(5):
                print "Number of Attempts exceeded Closing the connection"
                self.serversocket.close()
                sys.exit(0)
            elif auth_status ==str(6):
                # print "Password incorrect try again!!"
                while auth_status!=str(1):
                    print "Password incorrect try again!!"
                    if auth_status ==str(5):
                        print "Your maximum retries have reached"
                        self.serversocket.close()
                        sys.exit(0)
                    else:
                        sys.stdout.write(Common.recv_msg(self.serversocket))
                        Common.send_msg(self.serversocket,raw_input())
                        auth_status = Common.recv_msg(self.serversocket)
                print "Welcome to Chat Server!!"
                self.commands()
        except Exception as e:
            print "Caught Exception as ",e
            self.serversocket.close()
            sys.exit()
    
    def commands(self):
        input = True
        thread = threading.Thread(target=(self.new_socket_reciver))
        thread.deamon = True
        thread.start()
        
        while input:
            try:
                sys.stdout.write("$")
                command = raw_input()
                if not command:
                    continue
                Common.send_msg(self.serversocket,command)
                status = Common.recv_msg(self.serversocket)
                #Command is logout 
                if status ==str(8):
                    print "Logging you out"
                    # self.serversocket.close()
                    # sys.exit()
                    input=False
                #full parameters not defined in the command
                elif status==str(7):
                    print "Some parameter missing in the command"
                elif status==str(9):
                    print "Command not recognized"
                elif status==str(10):
                    pass
                elif status==str(11):
                    print "You are not Admin"
                else:
                    status = status.split(",")
                    for val in status:
                        sys.stdout.write(val+"\n")
                    sys.stdout.flush()
            except Exception as e:
                self.serversocket.close()
                print "Shutting down client",e
                break
        return
    #This thread runs in background and just passes async messages like
    #broadcast and private message!!
    def new_socket_reciver(self):
        while True:    
            try:
                r,_,_ = select.select([self.serversocket],[],[])
                if r:
                    data = Common.recv_msg(self.serversocket)
                    print data
                    if not data:
                        print "Server Down Switching off"
                        self.serversocket.close()
                        sys.exit()
                        break
                else:
                    continue
            except:
                self.serversocket.close()
                sys.exit()

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
