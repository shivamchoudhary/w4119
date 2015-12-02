import argparse
import Common
import sys
import cmd
class bfClient(object):
    """
    Class to manage all the clients.
    """
    
    def __init__(self, localport, timeout, ipaddress1, port1, weight1, *args):
        """
        param:localport Local port on which the client is hosted.
        param:timeout The timeout related with the client.
        param:ipaddress1 IP Address of First Neighbour.
        param:weight1 Weight of the link.
        param:*args Arguments (3 tuples) for optional neighbour.
        """
        self.ip = '127.0.0.1' #Each client is binded on localhost
        self.localport = localport
        self.timeout = timeout
        neighbourTable = Common.Table()
        neighbourTable.add_neighbour((ipaddress1, port1), (ipaddress1,weight1))
        #If the optional arguments are specified/else we have already added them.
        if args[0]:
            for arg in args:
                for triplets in arg:
                    ip, port, weight = triplets
                    neighbourTable.add_neighbour((ip, port), (ip,weight))
        self.wait_on_socket()
        console =Cli()
        console.cmdloop()
    
    def wait_on_socket(self):
        t1 = Common.DeploySocket(self.ip, self.localport)
        t1.start()

class Cli(cmd.Cmd):
    """
    Subclassed cmd for console Management!!
    """
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = "%>"
        self.doc_header="Distributed Bellman Ford"
        self.ruler="-"
    def cmdloop(self):
        try:
            cmd.Cmd.cmdloop(self)
        except TypeError:
            print "Wrong Syntax use help <command> to find correct usage."
            self.cmdloop()
    def do_LINKDOWN(self,ip_address,port):
        pass
    def help_LINKDOWN(self):
        print "Syntax: LINKDOWN {ip_address port}"
        print "This allows the user to destroy an existing link,i.e change",\
                'the link cost to infinity to the mentioned neighbour.'
    def do_LINKUP(self,ip_address,port):
        pass
    def help_LINKUP(self):
        print "Syntax: LINKUP {ip_address}"
        print "This allows the user to restore the link to the mentioned",\
                "neighbour to the original value after it was destroyed by,"\
                "LINKDOWN"

    def do_SHOWRT(self,arg):
        print "SHOWRT"
    def help_SHOWRT(self):
        print "Syntax: SHOWRT"
        print "This allows the user to view the current routuing table of",\
                " the client"
    def do_CLOSE(self):
        pass
    def help_CLOSE(self):
        print "Syntax: CLOSE"
        print "With this command the client process should close/shutdown."
    def default(self, line):
        print "Command Not recognized"
    def emptyline(self):
        pass
    def do_help(self, args):
        cmd.Cmd.do_help(self, args)
    def help_help(self):
        print "Syntax: help"
        print "Well it doesn't make sense to ask for help on help,Inception Maybe!!"
def main():
    parser = argparse.ArgumentParser(description='Bellman-Ford Distributed'
            'Algorithm')
    parser.add_argument("localport", type=int, help="local socket for "
            "binding!")
    parser.add_argument("timeout", type=int, help="timeout for the" 
            "client(in seconds)")
    parser.add_argument("ipaddress1", type=str, help="IP Address of a"
            "Neighbour")
    parser.add_argument("port1",type=int,help="Corresponding Port number" 
            "of Neighbour")
    parser.add_argument("weight1",type=float,help="A real number indicating"
            " cost of link")
    parser.add_argument("optional",nargs=argparse.REMAINDER,default=argparse.SUPPRESS,help="Other Arguments")
    args = parser.parse_args()
    args.optional = zip(*[args.optional[i::3] for i in range(3)])
    client = bfClient(args.localport, args.timeout, args.ipaddress1, 
            args.port1, args.weight1,args.optional)
        
if __name__=="__main__":
    main()
