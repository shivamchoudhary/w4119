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
pp = pprint.PrettyPrinter(indent=1)

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
        logging.debug("Adding ip:%s,port:%s,link:%s,weight:%s.",ip,port,
                link,weight)
        destination = ip+":"+str(port)
        Table.dvinfo['dvtable'][destination] = {
                "ip":ip,
                "port":port,
                "cost":float(weight),
                "link":link
                }
        if is_neighbour:
            Table.neighbourinfo['neighbours'][link] = {}
            Table.neighbourinfo['neighbours'][link]['cost'] = float(weight)
            Table.neighbourinfo['neighbours'][link]['link'] = link
            Table.neighbourinfo['neighbours'][link]['last_updated'] = \
                    time.time()
            Table.neighbourinfo['neighbours'][link]['ip'] = ip
            Table.neighbourinfo['neighbours'][link]['port'] = port
            Table.neighbourinfo['neighbours'][link]['active'] = True
    @staticmethod    
    def update(dict):
        """
        Extracts the IP and updates the last_updated variable for neighbour and
        dvtable. Also since this is an update message it restores the link as 
        well. I think I am going to run into trouble for doing this.
        """
        ip = dict['ip']
        port = dict['port']
        link = dict['link']
        dvtable = dict['dvtable']
        #update info wrt neigbour
        Table.neighbourinfo['neighbours'][link]['last_updated']= time.time()
        Table.neighbourinfo['neighbours'][link]['active'] = True
        Table.dvinfo['dvtable'][link]['cost'] = Table.neighbourinfo\
                ['neighbours'][link]['cost']
        Table.dvinfo['dvtable'][link]['link'] = Table.neighbourinfo\
                ['neighbours'][link]['link']
        logging.debug("Updating info for %s", link)
        Table.run_bellman(dict)
    
    @staticmethod    
    def run_bellman(recv_dvtable):
        self_cost = Table.dvinfo['dvtable'][recv_dvtable['link']]['cost']
        recv_dvtable['dvtable'].pop(Table.neighbourinfo['link']) #remove self
        for destination, metrics in recv_dvtable['dvtable'].iteritems():
            try:
                cur_cost = Table.dvinfo['dvtable'][destination]['cost']
                adv_cost = float(metrics['cost'])
                if (self_cost+adv_cost < cur_cost):
                    logging.debug("Less Path Cost available updating")
                    Table.dvinfo['dvtable'][destination]['cost'] = self_cost+\
                            adv_cost
                    Table.dvinfo['dvtable'][destination]['link'] = \
                            recv_dvtable['link']
            except KeyError:
                logging.debug("New Neighbour %s",destination)
                Table.add_neighbour((metrics['ip'],metrics['port']),\
                        (recv_dvtable['link'],self_cost+metrics['cost']))
    
class RecieveSocket(threading.Thread):
    """
    Primary work is to update the table with the information it recieves from 
    the sockets.
    """
    def __init__(self, commonq, port):
        """
        The reciever does not require ip because its on localhost
        param:ip The IP address on which it is to be binded
        param:port Port number on which it is to be binded
        """
        super(RecieveSocket, self).__init__()
        self.ip         = '127.0.0.1'
        self.port       = port
        self.lock       = threading.Lock()
        self.commonq    = commonq
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
        logging.debug("Reciever binding on (%s,%s) complete", self.ip, 
                self.port)
        while True:
            msg, _, _  = select.select([s],[],[])
            if msg:
                data = s.recvfrom(1024)
                recv_data = json.loads(data[0]) #JSON data with number of keys
                logging.debug("Recieved '%s' from %s", data[0], data[1])
                self.lock.acquire()
                Table.update(recv_data)
                self.lock.release()
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
    def run(self):
        while not self._dvchanged.wait(timeout=self.timeout):
            logging.debug('Self timeout (%s) sending route updates',
                    self.timeout)
            self.lock.acquire()
            for link in Table.neighbourinfo['neighbours'].keys():
                if Table.neighbourinfo['neighbours'][link]['active']:
                    if ((time.time()-Table.neighbourinfo['neighbours']\
                            [link]['last_updated'])> 3*self.timeout):
                        newlink = "Unknown"
                        Table.dvinfo['dvtable'][link]['active']=False
                        Table.dvinfo['dvtable'][link]['cost']=\
                                float("inf")
                        Table.dvinfo['dvtable'][link]['link']=newlink
                        Table.neighbourinfo['neighbours'][link]['active']=False
            dvtable = {
                    }
            for link in Table.dvinfo['dvtable'].keys():
                dvtable[link] = {}
                dvtable[link]['cost'] = Table.dvinfo['dvtable'][link]['cost']
                dvtable[link]['ip']  =Table.dvinfo['dvtable'][link]['ip']
                dvtable[link]['port'] = Table.dvinfo['dvtable'][link]['port']
            msg  = {
                    'ip':Table.neighbourinfo['ip'],
                    'port':Table.neighbourinfo['localport'],
                    'link': Table.neighbourinfo['link'],
                    'dvtable':dvtable
                    }
            for link in Table.neighbourinfo['neighbours'].keys():
                ip = Table.neighbourinfo['neighbours'][link]['ip']
                port = Table.neighbourinfo['neighbours'][link]['port']
                message  = json.dumps(msg)
                send(message, ip, int(port))
            self.lock.release()

            
    
class Message(object):
    """ 
    Messages exchanged between the clients. Each has data type.
    ROUTE_UPDATE    :(ip,port,dv) tuple
    LINK_UP         :(ip,port,dv)
    LINK_DOWN       :(ip,port)
    """
    ROUTE_UPDATE,LINK_UP,LINK_DOWN,CLOSE = range(4)
    def __init__(self, type, data=None):
        self.type = type
        self.data = data

class Handlers(object):
    def __init__(self,q):
        self.handlers = {
                Message.ROUTE_UPDATE:self._route_UPDATE
                }
        self.q = q
        self.run()
    def run(self):
        cmd = self.q
        self.handlers[cmd.type](cmd)
    def _route_UPDATE(self, (msg,ip,port)):
        msg.data['type'] = "ROUTE_UPDATE"
        data = json.dumps(msg.data)
        send(data,ip,port)

def send(msg, ip, port):
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.sendto(msg,(ip,port))
