import threading
import socket
import select
import cmd
import json
import time
import logging

def initLogger(level):
    #TODO : Add file config
    logging.basicConfig(
        format='Thread=[ %(threadName)s ]-level = [ %(levelname)s ]-'
        'Module=[ %(module)s ]-linenum=[ %(lineno)d ]- '
        'Function = [ %(funcName)s]-msg=[ %(message)s ]',
        level=level)

    
class Table(object):
    """
    A Generic class to hold the router Neighbour information.
    """
    def __init__(self):
        """
        Starts with an empty table dictionary
        """
        Table._dvchanged = False
        Table.table = {}
        Table.updated_table = {}
    def add_neighbour(self, (ip, port), (link, weight)):
        """
        A Neighbour is defined by <ip,port> tuple.
        param:ip,port IP address,Port tuple of the neighbour
        param:link IP address to reach,weight link and Weight to the neighbour
        """
        Table.updated_table[(ip, port)] = (link+":"+str(port), weight)
        self.update_table()
    @staticmethod
    def show_neighbours():
        """
        Shows the current neighbours of the client.
        return: table of neighbours.
        """
        return Table.updated_table
    def update_table(self):
        """
        For the time being it looks a clever way of doing things. Maintain two
        copies of the same table and update current one. After that compare 
        the two tables, if they are not equal set the table. We should not call
        it with add_neighbour because what if the user adds the same link!
        """
        if Table.table!=Table.updated_table:
            Table._dvchanged = True
        else:
            Table._dvchanged = False
        Table.table = Table.updated_table

class RecieveSocket(threading.Thread):
    """
    Subclassing thread to make it a bit more generic
    """
    def __init__(self):
        """
        param:ip The IP address on which it is to be binded
        param:port Port number on which it is to be binded
        """
        super(RecieveSocket, self).__init__()
        # self.ip = ip
        # self.port = port
        self._stop = threading.Event()
    def run(self):
        """
        Establish a listening port for the lifetime of the connection
        """
        logging.debug("Initializing Reciever Socket")
        # s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        # s.bind((self.ip, self.port))
        # while True:
            # r,a,b  = select.select([s],[],[],1)
            # if r:
                # data = s.recvfrom(1024)
            # if not r:
                # print "Timeout"
                # return None
            # if self._stop.is_set():
                # print "Shutting Down the Client"
                # s.close()
                # return

class SendSocket(threading.Thread):
    """ 
    The socket for sending the data between neighbours.It uses the Message
    class to dispatch appropriate functions. 
    """
    def __init__(self):
        super (SendSocket,self).__init__()
        self.handlers = {
                Message.ROUTE_UPDATE:self._route_UPDATE,
                Message.LINK_UP:self._link_UP,
                Message.LINK_DOWN:self._link_DOWN
        }
        self._dvchanged = threading.Event() #a flag to indicate dv has changed
    def run(self):
        logging.debug("Initializing sender socket")
    def _route_UPDATE(self):
        pass
    def _link_UP(self):
        pass
    def _link_DOWN(self):
        pass


class Message(object):
    """ Messages exchanged between the clients. Each has data type.
        ROUTE_UPDATE    :
        LINK_UP         :
        LINK_DOWN       :
    """
    ROUTE_UPDATE,LINK_UP,LINK_DOWN = range(3)
    def __init__(self,type,data=None):
        self.type = type
        self.data = data

      
