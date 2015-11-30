import sys
import argparse
import os
import Common
import socket
import select


class bfClient(object):
    """
    Class to manage all the clients.
    """

    def __init__(self,localport,timeout,ipaddress1,port1,weight1,*args):
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
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.ip, self.localport))
        neighbourTable = Common.Table()
        neighbourTable.add_neighbour((ipaddress1, port1),weight1)
        if args is not None:
            for arg in args:
                print arg


        print neighbourTable.show_neighbour()
    def converge(self):
        pass


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
    parser.add_argument("--optional",nargs='*',default = None,help="Other Arguments")
    args = parser.parse_args()
    print args
    if args.optional is not None:
        if len(args.optional)%3 !=0:
            raise ValueError ("Check Optional Arguments")
            sys.exit(2)
        else:
            args.optional = zip(*[args.optional[i::3] for i in range(3)])
            print args.optional
    client = bfClient(args.localport, args.timeout, args.ipaddress1, 
                args.port1, args.weight1,args.optional)
        
if __name__=="__main__":
    main()
