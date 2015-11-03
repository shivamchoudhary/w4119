import sys
import socket
import Common
import struct
import os

"""
Citations:
    1) Python's Hashlib(I used MD5 for this assignment) 
    https://docs.python.org/2/library/hashlib.html 
    2) Python's UDP Communication Wiki
    https://wiki.python.org/moin/UdpCommunication
"""
class Receiver(object):
    """
    A generic class which listens on listening port. 
    """

    def __init__(self, filename, listening_port, sender_IP, sender_port,
            log_filename_receiver):
        """
        Initializing the Receiver Object with all the parameters.
        """
        self.filename = filename                #Receiver outfile.
        self.listening_port = listening_port    #Recieverport number.
        self.sender_IP = sender_IP              #Send ACKs to sender.
        self.sender_port = sender_port          #sender port number.
        self.log_filename_receiver = log_filename_receiver # the log_file
        self.createSocket()
    def createSocket(self):
        """
        Create a socket and listen on that. Socket will be raw
        """
        recvsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        recvsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        recvsocket.bind(('127.0.0.1',41193))
        while True:
            data,addr = recvsocket.recvfrom(1024)
            print struct.unpack("!HHLLBBHHH", data[:20])
def main():
    """
    Obtains the parameters from the command line and raises a generic exception
    if some/all are missing.
    """
    try:
        filename                = str(sys.argv[1]) 
        listening_port          = int(sys.argv[2])
        sender_IP               = sys.argv[3]
        sender_port             = int(sys.argv[4])
        log_filename_receiver   = str(sys.argv[5])
        #TODO add the case in which the logging is done on stdout
        Receiver(filename, listening_port, sender_IP, sender_port,
                log_filename_receiver)
    except IndexError:
        print "Some parameter(s) is/are missing invoke in the following format",\
                "<filename> <listening_port> <sender_IP> <sender_port> ",\
                "<log_filename_receiver>"
    except KeyboardInterrupt:
        print 'ctrl-c pressed !!'
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)


if __name__ =="__main__":
    main()
