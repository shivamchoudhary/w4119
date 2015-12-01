import time
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
