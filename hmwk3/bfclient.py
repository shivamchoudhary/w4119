import argparse
import Common
import cmd
import datetime
import threading
import time
import logging
from threading import Lock
import Queue
class bfClient(threading.Thread):
    """
    Class to manage all the clients. It starts the CLI Loop'
    """
    def __init__(self, localport, timeout, ipaddress1, port1, weight1, *args):
        """
        param:localport Local port on which the client is hosted.
        param:timeout The timeout related with the client.
        param:ipaddress1 IP Address of First Neighbour.
        param:weight1 Weight of the link.
        param:*args Arguments (3 tuples) for optional neighbour.
        """
        super(bfClient, self).__init__()
        self._stop = threading.Event()
        self.ip = '127.0.0.1' #Each client is binded on localhost
        self.localport = localport
        self.timeout = timeout
        self.neighbourTable = Common.Table()
        self.neighbourTable.add_neighbour((ipaddress1, port1), 
                (ipaddress1, weight1))
        #If the optional arguments are specified/else we have already added 
        # them.
        if args[0]:
            for arg in args:
                for triplets in arg:
                    ip, port, weight = triplets
                    logging.debug("Adding %s with %s",(ip, port),(ip, weight))
                    self.neighbourTable.add_neighbour((ip, port), (ip, weight))
        logging.info("Initialized Client Current table is %s", 
                self.neighbourTable.table)
    def run(self):
        console =Cli()
        console.cmdloop()
class Cli(cmd.Cmd):
    """
    Subclassed cmd for console Management!!
    """
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.SUPPORTED_COMMANDS = ['showrt','linkup','linkdown','close','help',
                'tip']
        self.prompt     = "%>"
        self.doc_header ="Distributed Bellman Ford"
        self.ruler      ="-"
        self.intro      = 'Welcome to Bellman Ford Router Shell. Type help'
        'or list Commands. Bonus tip: You can enter them in *any* case'
        logging.info("Initializing CLI with (%s)",self.SUPPORTED_COMMANDS)
    def cmdloop(self):
        try:
            cmd.Cmd.cmdloop(self)
        except TypeError as e:
            print "Wrong Syntax use help <command> to find correct usage.",e
            self.cmdloop()
    def precmd(self,line):
        logging.debug("Input:'%s'",line)
        line = line.lower()
        return cmd.Cmd.precmd(self, line)
    def do_linkdown(self,ip_address,port):

        pass
    def help_linkdown(self):
        print "Syntax: LINKDOWN {ip_address port}"
        print "This allows the user to destroy an existing link,i.e change",\
                'the link cost to infinity to the mentioned neighbour.'
    def do_linkup(self, ip_address, port):
        pass
    def help_linkup(self):
        print "Syntax: LINKUP {ip_address}"
        print "This allows the user to restore the link to the mentioned",\
                "neighbour to the original value after it was destroyed by,"\
                "LINKDOWN"
    def do_showrt(self, arg):
        neighbourTable = Common.Table.show_neighbours()
        print "{} Distance vector list is".format(
                datetime.datetime.now().strftime("%b %d %Y %H:%M:%S"))
        
        for k,v in neighbourTable.iteritems():
            dst     = k[0]+":"+str(k[1])
            cost    = v['cost']
            link    = v['link']
            if arg:
                last_updated = datetime.datetime.fromtimestamp(
                        v['last_updated']).strftime('%Y-%m-%d %H:%M:%S')
                print "Destination = {}, Cost = {}, Link = ({}), Last Updated = {}".format(dst, cost, link, last_updated)
            else: 
                print "Destination = {}, Cost = {}, Link = ({})".format(
                        dst, cost, link)
            
    def help_showrt(self):
        print "Syntax: SHOWRT {optional any argument}"
        print "This allows the user to view the current routing table of",\
                " the client. If supplied with any arg last_update"
    def complete_default(self, text, line, begidx, endidx):
        if not text:
            completions = self.SUPPORTED_COMMANDS[:]
        else:
            completions = [f
                    for f in self.SUPPORTED_COMMANDS if f.startswith(text)
                    ]
        return completions
    def do_close(self):
        pass
    def help_close(self):
        print "Syntax: CLOSE"
        print "With this command the client process should close/shutdown."
    def do_tip(self,line):
        print "1) You can type help <command_name> to get syntax and help."
        print "2) You can type in any case."
        print "3) You can use tab completions try it seriously its awesome"
    
    def default(self, line):
        print "Command Not recognized,try help or press <tab>"
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
    parser.add_argument("port1", type=int, help="Corresponding Port number" 
            "of Neighbour")
    parser.add_argument("weight1", type=float, help="A real number indicating"
            " cost of link")
    parser.add_argument("optional", nargs=argparse.REMAINDER, 
            default=argparse.SUPPRESS, help="Other Arguments")
    args = parser.parse_args()
    args.optional = zip(*[args.optional[i::3] for i in range(3)])
    #initialize all the queues here!!
    #Reciever Queue
    reciever_q = Queue.Queue()
    #Sender Queue
    neighbourTable_q = Queue.Queue()
    #initialize all the threads down here !!
    client = bfClient(args.localport, args.timeout, args.ipaddress1, 
    args.port1, args.weight1,args.optional)
    client.start()
    sendsocket = Common.SendSocket(reciever_q,args.timeout)
    sendsocket.start()
    recieversocket = Common.RecieveSocket(args.localport)
    recieversocket.start()
    #TODO
    # Add Support to capture ctrl-c events in thread
    sendsocket.join()
if __name__=="__main__":
    Common.initLogger(logging.DEBUG)
    main()