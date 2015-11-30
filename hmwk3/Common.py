
class Commands(object):
    
    
    def __init__(self):
        pass
class Table(object):
    """
    A Generic class to hold the router Neighbour information.
    """
    
    def __init__(self):
        self.table = {}
    def add_neighbour(self, ip, port):
        """
        A Neighbour is defined by <ip,port> tuple.
        param:ip IP address of the neighbour
        param:port Remote port of the neighbour
        """
        self.table[ip] = port
        
