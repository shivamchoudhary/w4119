import sys
import socket
import Common

configuration = Common.read_config()

class CreateServer(object):
    """
    Creates a server at IP and specifed port.
    """
    def __init__(self, host, port):
        self.host = host
        self.port = port
        server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            server.bind((host,port))
        except socket.error as e:
            print ("Binding failed. Error:%s",msg)
            sys.exit()
        server.listen(10)
        print "Server Running"
        while 1:
            conn,add  = server.accept()
            print ('Connected with ', add)
        server.close()
a = CreateServer('127.0.0.1',8080)




