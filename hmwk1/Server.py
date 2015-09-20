import sys
import socket
import Common
import thread
import argparse

configuration = Common.read_config()

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
            sys.exit()
        serversocket.listen(5)
        print "Server Running"
        while 1:
            try:
                (clientsocket,address) = serversocket.accept()
                print "Connected to ",address
                thread.start_new_thread(handler,(clientsocket,address))
            except KeyboardInterrupt:
                serversocket.close()
   
def handler(clientsock,addr):
    while 1:
        clientsock.send("Username:")
        username = clientsock.recv(1024)
        clientsock.send("Password:")
        password  = clientsock.recv(1024)
    clientsock.close()

def main():
    try:
        port = int(sys.argv[1])
    except IndexError:
        print "Please specify a port number to bind the server."
        sys.exit()
    CreateServer(port)
if __name__=="__main__":
    main()





