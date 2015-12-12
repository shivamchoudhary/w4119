import threading
import socket
import select
import cmd
import json
import time
import logging
import Queue
import datetime
def initLogger(level):
    #unified logging module for all the libraries in this folder!.
    logging.basicConfig(
        format='Thread=[ %(threadName)s ]-level = [ %(levelname)s ]-'
        'Module=[ %(module)s ]-linenum=[ %(lineno)d ]- '
        'Function = [ %(funcName)s]-msg=[ %(message)s ]',
        level=level, filename="client.log", filemode="w")
    
class Table(object):
    """
    A Generic class to hold the router Neighbour information.
    """
    def __init__(self,ip,port):
        """
        Starts with an empty table dictionary
        """
        Table.table = {}
        Table.selfname = ip+":"+str(port)
    @staticmethod
    def add_neighbour((ip, port), (link, weight)):
        """
        A Neighbour is defined by <ip,port> tuple.
        param:ip,port IP address,Port tuple of the neighbour
        param:link IP address to reach,weight link and Weight to the neighbour
        Updates the Table with the last_updated value
        """
        logging.debug("Initializing (ip=%s),(port=%s),(link=%s),(weight=%s)",
                ip, port, link, weight)
        Table.table[ip+":"+str(port)] = {
                "cost":float(weight),
                "link":link+":"+str(port),
                "last_updated":time.time(),
                "active":True
                }
    
    @staticmethod    
    def update(dict):
        """
        Extracts the IP and updates the last_updated variable for that hostname
        """
        ip = dict['ip']
        port = dict['port']
        try:
            logging.debug("Updating last_updated for (%s:%s)",ip,port)
            Table.table[(ip,port)]["last_updated"] = time.time()
        except KeyError:
            """
            New entry add to table
            """
            logging.debug("Entry for (%s:%s) does not exists,adding",ip,port)
            Table.add_neighbour((ip, port), (dict['link'], dict['cost']))
        Table.run_bellman(dict)
    @staticmethod    
    def run_bellman(dict):
        for hostname in dict['dvtable'].keys():
            if hostname in Table.table.keys():
                print hostname
                present_cost = Table.table[hostname]['cost']
                advertised_cost = dict['dvtable'][hostname]['cost']
                peer = dict['link']
                mycost = Table.table[peer]['cost']
                totalcost = mycost+advertised_cost
                if totalcost < present_cost:
                    print "Deal"


    @staticmethod
    def show_neighbours():
        """
        Shows the current neighbours of the client.
        return: dvtable of neighbours.
        """
        return Table.table

class RecieveSocket(threading.Thread):
    """
    Primary work is to update the table with the information it recieves from 
    the sockets.
    """
    def __init__(self, port):
        """
        The reciever does not require ip because its on localhost
        param:ip The IP address on which it is to be binded
        param:port Port number on which it is to be binded
        """
        super(RecieveSocket, self).__init__()
        self.ip = '127.0.0.1'
        self.port = port
        self.lock = threading.Lock()
        self._stop = threading.Event()
    def run(self):
        """
        Establish a listening port for the lifetime of the connection
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.bind((self.ip, self.port))
        except socket.error as e:
            logging.error("Error %s while binding", e)
        logging.debug("Reciever binding on (%s,%s) complete", self.ip, self.port)
        while True:
            msg, _, _  = select.select([s],[],[])
            if msg:
                data = s.recvfrom(1024)
                recv_data = json.loads(data[0]) #JSON data with number of keys
                logging.debug("Recieved '%s' from %s", data[0], data[1])
                self.lock.acquire()
                Table.update(recv_data)
                self.lock.release()
            if self._stop.is_set():
                print "Shutting Down the Client"
                s.close()
                return
            time.sleep(0.2)

class SendSocket(threading.Thread):
    """ 
    The socket for sending the data between neighbours.It uses the Message
    class to dispatch appropriate functions.Waits till timeout seconds or if
    dv has changed!
    """
    #TODO
    # Add a way to take neighbourTable and parse it
    def __init__(self, timeout):
        super (SendSocket, self).__init__()
        self.handlers = {
                Message.ROUTE_UPDATE:self._route_UPDATE,
                Message.LINK_UP:self._link_UP,
                Message.LINK_DOWN:self._link_DOWN
        }
        self.timeout        = timeout
        self._dvchanged     = threading.Event() #event dv has changed
        self.stoprequest    = threading.Event()
        self.lock           = threading.Lock()
        #TODO Add the port name and ip address mapping here.
        logging.debug("Initializing sender socket on (%s:%s)")

    def run(self):
        while not self._dvchanged.wait(timeout=self.timeout):
            logging.debug('Self timeout (%s) sending route updates',
                    self.timeout)
            self.lock.acquire()
            neighbour = Table.table
            for hostname, attributes in neighbour.iteritems():
                if (time.time() - attributes['last_updated']) > 3*self.timeout:
                    neighbour[hostname]['active'] = False
            self.lock.release()
            time.sleep(0.2)
    def _route_UPDATE(self):
        pass
    def _link_UP(self):
        pass
    def _link_DOWN(self):
        pass

class Message(object):
    """ 
    Messages exchanged between the clients. Each has data type.
    ROUTE_UPDATE    :(ip,port,dv) tuple
    LINK_UP         :(ip,port,dv)
    LINK_DOWN       :(ip,port)
    """
    ROUTE_UPDATE,LINK_UP,LINK_DOWN = range(3)
    def __init__(self,type,data=None):
        self.type = type
        self.data = data

      
