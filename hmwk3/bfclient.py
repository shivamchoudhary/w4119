import sys
import os


class bfClient(object):

    def __init__(self):
        self.ip = '127.0.0.1'






def main():
    try:
        localport = int(sys.argv[1])
        timeout = int(sys.argv[2])
    except IndexError:
        print "python bfclient.py <localport> <timeout> <ipaddress1> <port1>"
        "<weight1> ... "
        sys.exit(2)
    except KeyboardInterrupt:
        print "Control -C pressed!!"
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

