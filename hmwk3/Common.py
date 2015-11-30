
class Commands(object):
    
    
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
        #TODO:
        # change the table to some hashed key or some tuple entry to incorporate
        # weight!!

        self.table = {}
    def add_neighbour(self, ip, port):
        """
        A Neighbour is defined by <ip,port> tuple.
        param:ip IP address of the neighbour
        param:port Remote port of the neighbour
        """
        self.table[ip] = port
    def show_neighbour(self):
        """
        Shows the current neighbours of the client.
        return: table of neighbours.
        """
        return self.table
