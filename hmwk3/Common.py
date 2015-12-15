import threading
import socket
import select
import cmd
import json
import time
import logging
import Queue
import datetime
import pprint
pp = pprint.PrettyPrinter(indent=2)
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
    def __init__(self, ip, port):
        """
        Starts with an empty table dictionary
        """
        self.ip = ip
        self.port = port
        
        Table.dvinfo = {
                "dvtable":{
                    }
                }


        Table.neighbourinfo = {
                "ip":self.ip,
                "localport":self.port,
                "link":self.ip+":"+str(self.port),
                "neighbours":{
                    }
                }
    @staticmethod
    def add_neighbour((ip, port), (link, weight), is_neighbour =False):
        """
        A Neighbour is defined by <ip,port> tuple.
        param:ip,port IP address,Port tuple of the neighbour
        param:link IP address to reach,weight link and Weight to the neighbour
        Updates the Table with the last_updated value
        """
        Table.dvinfo['dvtable'][link] = {}
        dvtable_info = {
                'ip':ip,
                'port':port,
                'cost':float(weight),
                'link':link
                }
        Table.dvinfo['dvtable'][link] = dvtable_info
        if is_neighbour:
            Table.neighbourinfo['neighbours'][link] = {}
            Table.neighbourinfo['neighbours'][link]['cost'] = float(weight)
            Table.neighbourinfo['neighbours'][link]['link'] = link
            Table.neighbourinfo['neighbours'][link]['last_updated'] = \
                    time.time()
            Table.neighbourinfo['neighbours'][link]['active'] = True
    @staticmethod    
    def update(dict):
        """
        Extracts the IP and updates the last_updated variable for neighbour and
        dvtable
        """
        ip = dict['ip']
        port = dict['port']
        link = dict['link']
        dvtable = dict['dvtable']
        #update info wrt neigbour
        Table.neighbourinfo['neighbours'][link]['last_updated']= time.time()
        Table.neighbourinfo['neighbours'][link]['active'] = True
        Table.run_bellman(dict)
    
    @staticmethod    
    def run_bellman(recv_dvtable):
        self_cost = Table.information['neighbours'][recv_dvtable['link']]['cost']
        recv_dvtable['dvtable'].pop(Table.information['link']) #to remove self
        for destination, metrics in recv_dvtable['dvtable'].iteritems():
            try:
                cur_cost = Table.information['dvtable'][destination]['cost']
                adv_cost = float(metrics['cost'])
                if (self_cost + adv_cost < cur_cost):
                    Table.information['dvtable'][destination]['cost'] = \
                            self_cost+adv_cost
                    Table.information['dvtable'][destination]['link'] = \
                            recv_dvtable['link']
            except KeyError:
                Table.add_neighbour((metrics['ip'],metrics['port']),
                        (recv_dvtable['link'], metrics['cost']+self_cost))

    @staticmethod
    def show_neighbours():
        """
        Shows the current neighbours of the client.
        return: dvtable of neighbours.
        """
        return Table.information['dvtable']

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
        self.timeout        = timeout
        self._dvchanged     = threading.Event() #event dv has changed
        self.stoprequest    = threading.Event()
        self.lock           = threading.Lock()
        logging.debug("Initializing sender socket on (%s:%s)")

    def run(self):
        while not self._dvchanged.wait(timeout=self.timeout):
            logging.debug('Self timeout (%s) sending route updates',
                    self.timeout)
            self.lock.acquire()
            neighbours = Table.information['neighbours']
            for neighbour in neighbours:
                if neighbours[neighbour]['active']:
                    if ((time.time()- neighbours[neighbour]['last_updated'])>
                            3*self.timeout):
                        logging.debug("3*Timeout making (%s) inactive",neighbour)
                        Table.information['neighbours'][neighbour]\
                                ['active']= False
            self.lock.release()
            time.sleep(0.2)
    
class Message(object):
    """ 
    Messages exchanged between the clients. Each has data type.
    ROUTE_UPDATE    :(ip,port,dv) tuple
    LINK_UP         :(ip,port,dv)
    LINK_DOWN       :(ip,port)
    """
    ROUTE_UPDATE,LINK_UP,LINK_DOWN,CLOSE = range(4)
    def __init__(self,type,data=None):
        self.type = type
        self.data = data

