
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
        self.table[ip] = port
        
