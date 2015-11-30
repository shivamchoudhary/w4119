import sys
import argparse
import os

class bfClient(object):
    """
    Class to manage all the clients.
    param:
    """

    def __init__(self,port,timeout,ipaddress1,port1,weight1,*args):
        self.ip = '127.0.0.1' #Each client is binded on localhost
        self.port = port
        self.timeout = timeout
        self.ipaddress1 = ipaddress1
        self.port1 = port1
    def converge(self):
        pass


def main():
    parser = argparse.ArgumentParser(description='Bellman-Ford Distributed'
            'Algorithm')
    parser.add_argument("localport", type=int, help="local socket for binding!")
    parser.add_argument("timeout", type=int, help="timeout for the client(in seconds)")
    parser.add_argument("ipaddress1", type=str, help="IP Address of a Neighbour")
    parser.add_argument("port1",type=int,help="Corresponding Port number of Neighbour")
    parser.add_argument("weight1",type=float,help="A real number indicating cost of link")
    parser.add_argument("optional",nargs='*',default=None,help="Other Arguments")
    args = parser.parse_args()
    if len(args.optional)%3 !=0:
        raise ValueError ("Check Optional Arguments")
        sys.exit(2)
    else:
        print args
if __name__=="__main__":
    main()
