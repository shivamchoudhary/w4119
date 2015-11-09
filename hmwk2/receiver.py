import sys
import socket
import Common
import struct
import os
import time
import threading
"""
Citations:
    1) Python's UDP Communication Wiki
    https://wiki.python.org/moin/UdpCommunication
"""
class Receiver(object):
    """
    A generic class which listens on listening port. 
    """

    def __init__(self, filename, listening_port, sender_IP, sender_port,
            log_filename_receiver):
        """
        Initializing the Receiver state.
        """
        self.filename = open(filename,'w+')      #Receiver outfile.
        self.listening_port = listening_port    #Recieverport number.
        self.sender_IP = sender_IP              #Send ACKs to sender.
        self.sender_port = sender_port          #ACK port number 20001.
        self.log_filename_receiver = log_filename_receiver # the log_file
        self.expected_seqnum = 1
        self.createSocket()
    
    def createSocket(self):
        """
        Create a socket and listen on that. Socket will be raw
        """
        recvsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        recvsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        recvsocket.bind(('localhost', self.listening_port))
        acksocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        address = ('localhost',20001)
        opened = False
        while True:
            data, addr = recvsocket.recvfrom(1024)
            sport, dport, seq, ack, off, flags, win, sum, urp = struct.unpack(
                    "!HHLLBBHHH", data[:20])
            expected_checksum = sum
            #required because at sender checksum is computed with sum=0
            sum = 0
            tcp_header = struct.pack("!HHLLBBHHH",sport,dport,seq,ack,off,flags,
                    win,sum,urp)
            msg = data[20:]
            checksum = Common.checksum((tcp_header+msg))
            if checksum !=expected_checksum:
                print "Checksum failed"
            else:
                if self.expected_seqnum == seq:
                    print time.time(), self.sender_IP, seq, ack, flags
                    self.filename.write(msg)
                    self.expected_seqnum +=len(msg)
                    try:
                        if not opened:
                            acksocket.connect(address)
                            opened = True
                        # time.sleep(3)
                        acksocket.sendall(str(seq))
                        if flags ==1:
                            self.filename.close()
                            sys.exit()
                    except Exception as error:
                        print "Caught: %s",error

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
        # t1 = ackSender()
        # t1.start()
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
