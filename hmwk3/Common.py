import time
import threading
import socket
import sys
class Commands(object):
    
    
    def __init__(self):
        pass
class Print(object):
    def __init__(self):
        pass
        
class Table(object):
    """
    A Generic class to hold the router Neighbour information.
    """
    
    def __init__(self):
        """
        Starts with an empty table dictionary
        """
        self.table = {}
    def add_neighbour(self, (ip,port), weight):
        """
        A Neighbour is defined by <ip,port> tuple.
        param:ip,port IP address,Port tuple of the neighbour
        param:weight Weight of the link to the neighbour
        """
        self.table[(ip,port)] = float(weight)
    def show_neighbours(self):
        """
        Shows the current neighbours of the client.
        return: table of neighbours.
        """
        return self.table

class DeploySocket(threading.Thread):
    """
    Subclassing thread to make it a bit generic
    """
    def __init__(self, ip, port):
        """
        param:ip The IP address on which it is to be binded
        param:port Port number on which it is to be binded
        """
        super(DeploySocket, self).__init__()
        self.ip = ip
        self.port = port
        self._stop = threading.Event()
    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        s.bind((self.ip,self.port))
        while True:
            try:
                s.recvfrom(1024)
                sys.stdout.write("%$")
            except socket.error:
                if self._stop.is_set():
                    print "Shutting Down the Client"
                    s.close()
                    return
