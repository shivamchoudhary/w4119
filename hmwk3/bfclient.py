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
    def __init__(self, commonq, localport, timeout, ipaddress1, port1, 
            weight1, *args):
        """
        param:localport Local port on which the client is hosted.
        param:timeout The timeout related with the client.
        param:ipaddress1 IP Address of First Neighbour.
        param:weight1 Weight of the link.
        param:*args Arguments (3 tuples) for optional neighbour.
        """
        super(bfClient, self).__init__()
        self.ip = '127.0.0.1' #Each client is binded on localhost
        self.commonq = commonq
        self.localport = localport
        self.timeout = timeout
        self.info = Common.Table(self.ip, self.localport)
        self.info.add_neighbour((ipaddress1, port1), 
                (ipaddress1+":"+str(port1), weight1), is_neighbour=True)
        #If optional arguments are specified/else already added them.
        if args[0]:
            for arg in args:
                for triplets in arg:
                    ip, port, weight = triplets
                    logging.debug("Adding %s with %s",(ip, port),
                            (ip+":"+str(port), weight))
                    self.info.add_neighbour((ip, port), (ip+":"+str(port),
                        weight), is_neighbour=True)
        logging.info("Neighbour Table is %s",self.info.neighbourinfo)
        logging.info("DV Table is %s",self.info.dvinfo)
    def run(self):
        console = Cli()
        console.cmdloop()
        data = "close"
        self.commonq.put(data)

class Cli(cmd.Cmd):
    """
    CLI for console Management!!
    """
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.SUPPORTED_COMMANDS = [
                'showrt','linkup','linkdown','close','help','tip',
                'showneigbours'
                ]
        self.prompt     = "%>"
        self.doc_header = "Distributed Bellman Ford"
        self.ruler      = "-"
        self.intro      = 'Welcome to Bellman Ford Router Shell. Type help'\
        ' for list Commands. Bonus tip: You can enter them in *any* case'
        logging.info("Initializing CLI with (%s)", self.SUPPORTED_COMMANDS)
    
    def cmdloop(self):
        try:
            cmd.Cmd.cmdloop(self)
        except TypeError as e:
            print "Wrong Syntax use help <command> to find correct usage.",e
            self.cmdloop()
    def precmd(self, line):
        """
        Converts each line to lower case so that any type of input accepted
        """
        logging.debug("Input:'%s'", line)
        line = line.lower()
        return cmd.Cmd.precmd(self, line)
    
    def do_linkdown(self, line):
        """
        param line: the input neighbour which has died. 
        Sets link distance to "inf"
        """
        try:
            (ip , port) = line.split(" ")
            link = ip+":"+port
            if link in Common.Table.neighbourinfo['neighbours'].keys():
                newlink = "Unknown"
                Common.Table.dvinfo['dvtable'][link]['cost'] = \
                        float("inf")
                Common.Table.dvinfo['dvtable'][link]['link'] = newlink
                Common.Table.neighbourinfo['neighbours'][link]['last_updated'] =\
                        time.time()
                Common.Table.neighbourinfo['neighbours'][link]['active']=False
            else:
                print "The link {} is not your direct neighbour".format(link)
        except ValueError:
            print "Wrong Syntax use help <command> to find correct usage."
            self.cmdloop()
    
    def help_linkdown(self):
        print "Syntax: LINKDOWN {ip_address port}"
        print "This allows the user to destroy an existing link,i.e change",\
                'the link cost to infinity to the mentioned neighbour.'
    
    def do_linkup(self, line):
        try:
            (ip, port) = line.split(" ")
            link = ip+":"+port
            if link not in Common.Table.neighbourinfo['neighbours'].keys():
                print " Can't do linkup {} is not your neighbour".format(link)
            else:
                cost = Common.Table.neighbourinfo['neighbours'][link]['cost']
                oldlink = Common.Table.neighbourinfo['neighbours'][link]['link']
                Common.Table.neighbourinfo['neighbours'][link]['active']=True
                Common.Table.neighbourinfo['neighbours'][link]['last_updated']\
                        =time.time()
                Common.Table.dvinfo['dvtable'][link]['cost'] = cost
                Common.Table.dvinfo['dvtable'][link]['link'] = oldlink
                logging.debug("Restoring cost %s for %s",cost,link )
        except ValueError:
            print "Wrong Syntax use help <command> to find correct usage."
            self.cmdloop()
            
    def help_linkup(self):
        print "Syntax: LINKUP {ip_address}"
        print "This allows the user to restore the link to the mentioned",\
                "neighbour to the original value after it was destroyed by,"\
                "LINKDOWN"
    
    def do_showrt(self, arg):
        print "{} Distance vector list is".format(
                datetime.datetime.now().strftime("%b %d %Y %H:%M:%S"))
        for k, v in Common.Table.dvinfo['dvtable'].iteritems():
            dst     = k
            cost    = v['cost']
            link    = v['link']
            if arg:
                status = v['active']
                print "Destination = {}, Cost = {},"\
                        " Link = ({}), Active = {}"\
                        .format(dst, cost, link, status)
            else: 
                print "Destination = {}, Cost = {}, Link = ({})".format(
                        dst, cost, link)
            
    def do_showneighbours(self, arg):
        """ Syntax: SHOWRT {optional any argument}
        This allows the user to view the current routing table of",the client. 
        If supplied with any arg last_update,shows the neighbours of the 
        particular client.
        """
        neighbourTable = Common.Table.neighbourinfo['neighbours']
        for k, v in neighbourTable.iteritems():
            print "Link = {}, Active = {}".format(k,v['active'])

    def complete_default(self, text, line, begidx, endidx):
        if not text:
            completions = self.SUPPORTED_COMMANDS[:]
        else:
            completions = [f
                    for f in self.SUPPORTED_COMMANDS if f.startswith(text)
                    ]
        return completions
    def do_close(self,line):
        """Syntax: close, With this command the Client process closes/shutsdown
        ."""
        print "Bye from Shell!!"
        return True
    def do_tip(self,line):
        print "1) You can type help <command_name> to get syntax and help."
        print "2) You can type in any case."
        print "3) You can use tab completions try it seriously its awesome"
    
    def default(self, line):
        print "Command Not recognized,try help or press <tab>"
    
    def emptyline(self):
        pass

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
    #Queue
    #CLI thread
    commonq = Queue.Queue()
    client = bfClient(commonq,args.localport, args.timeout, args.ipaddress1,
            args.port1, args.weight1, args.optional)
    client.start()
    #Sender thread
    sendsocket = Common.SendSocket(args.timeout)
    sendsocket.start()
    #Reciever Thread
    recieversocket = Common.RecieveSocket(commonq,args.localport)
    recieversocket.start()
    #TODO
    # Add Support to capture ctrl-c events in thread
if __name__=="__main__":
    Common.initLogger(logging.DEBUG)
    main()
