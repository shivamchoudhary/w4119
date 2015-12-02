import time
import threading
import socket
import sys
import select
import cmd
import json
        
class Table(object):
    """
    A Generic class to hold the router Neighbour information.
    """
    def __init__(self):
        """
        Starts with an empty table dictionary
        """
        self.table = {}
    def add_neighbour(self, (ip, port), (link, weight)):
        """
        A Neighbour is defined by <ip,port> tuple.
        param:ip,port IP address,Port tuple of the neighbour
        param:link IP address to reach,weight link and Weight to the neighbour
        """
        self.table[(ip, port)] = (link, weight)
    @staticmethod
    def show_neighbours():
        """
        Shows the current neighbours of the client.
        return: table of neighbours.
        """
        return self.table

class DeploySocket(threading.Thread):
    """
    Subclassing thread to make it a bit more generic
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
        s.bind((self.ip, self.port))
        while True:
            r,a,b  = select.select([s],[],[],5)
            if r:
                data = s.recvfrom(1024)
            if not r:
                print "Timeout"
                return None
            if self._stop.is_set():
                print "Shutting Down the Client"
                s.close()
                return

class Message(object):
    def __init__(self):
        pass


