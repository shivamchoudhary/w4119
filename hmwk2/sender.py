import sys
import socket
import Common
import struct
import os
import threading
"""
Citations:
"""
"""
Sender FSM:-
1)Architecture as per assignment:-
            Proxy(port 41192)
              /       \                
          sender-----receiver
       (127.0.0.1) (127.0.0.1)
______________________________________________________________________________
Sender Side FSM:-
##############################################################################
Initialize:
    N = window_size * MSS
    InitialSeqNum = 0
    NextSeqNum = 1
    SendBase = InitialSeqNum
##############################################################################
event:udt_send
    if NextSeqNum <SendBase +N:
        pkt = make_pkt(data)
        send_data(pkt)
        if (timer not running):
            start_timer
        NextSeqNum +=len(data)
event:timeout:
    retransmit from send_base
    start_timer
event: ACK recieved:
    if y>SendBase:
        SendBase=y
        if no currently unack seg:
            start timer
______________________________________________________________________________`
Receiver Side FSM:-
##############################################################################
Initialize:
    ExpectedSeqNumber = 0
event:recv_data and finnotset
    if x==ExpectedSeqNumber:
        write_to_file
        send_ack(ExpectedSeqNumber+len(data))
        ExpectedSeqNumber+=len(data)
event:FIN BIT set:
    write_to_file
    send_ack()

2)Usage: 
    (Proxy Mode)
    make lnkemu
    make testsender
    make reciever
    (Without Proxy)
    make sender
    make reciever
"""
class Sender(object):

    def __init__(self, filename, remote_IP, remote_port, ack_port_num,
            log_filename, window_size):
        # Initializing Sender state command line variables.
        self.filename       = filename      #sent filename,default 'file.txt'
        self.remote_IP      = remote_IP     #IP for sending,default 127.0.0.1
        self.remote_port    = remote_port   #Port number
        self.ack_port_num   = ack_port_num  #listening port,default 20001
        self.log_filename   = log_filename  #log file ,default send_logfile.txt
        self.window_size    = window_size   #window size,default 1152 bytes
        # Load file
        self.file           = open(self.filename)   #open the file to be sent.
        # Packet level
        self.MSS            = 576           #set maximum segment size to 576
        self.N              = self.MSS*self.window_size #set N to MSS*window
        self.InitialSeqNum  = 0
        self.NextSeqNum     = 1
        self.SendBase       = self.InitialSeqNum
        #Initialize the socket for udt_send
        self.udt_sock       = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,
                        socket.IPPROTO_UDP)
        self.udt_sock.connect((self.remote_IP, self.remote_port))
        self.udt_send() 
    def udt_send(self):
        """
        Unreliably send the data through the channel!!
        """
        if self.NextSeqNum <self.SendBase+self.N:
            pkt = self.make_pkt()
            self.send_data(pkt)
            # if timer.status!=True:
                # timer.start()
    def make_pkt(self):
        self.file.seek(self.NextSeqNum -1)
        msg = self.file.read(self.MSS)
        pkt = Common.Packet(self.ack_port_num, self.remote_port, 
                self.NextSeqNum,0,msg)
        return pkt.pack()
    def send_data(self, pkt):
        """
        This just sends the packet over the link!!
        """
        Common.send_msg(self.udt_sock, pkt) 
    def timeout(self):
        pass
    def rdt_rcv(self):
        acksocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        acksocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            acksocket.bind(('localhost', self.ack_port_num))
        except socket.error as error:
            print ("Socket binding failed with error %s", error)
        while True:
            acksocket.listen(1)
    def seekfile(self, seek_length=0):
        """
        Seeks the filename by window size,takes optional argument for 
        seeking
        """
        self.file.seek(seek_length)
        current_window = self.file.read(self.window_size)
        return current_window


def main():
    try:
        filename        = str(sys.argv[1])
        remote_IP       = sys.argv[2]
        remote_port     = int(sys.argv[3])
        ack_port_num    = int(sys.argv[4])
        log_filename    = str(sys.argv[5])
        window_size     = int(sys.argv[6])
        Sender(filename, remote_IP, remote_port, ack_port_num, log_filename, 
                window_size)
    #TODO Adding support when the log_filename=stdout log to stdout.
    except IndexError:
        print "python sender.py <filename> <remote_IP> <remote_port>",\
        "<ack_port_num> <log_filename> <window_size>" 
        sys.exit(2)
    except KeyboardInterrupt:
        print 'Control -C pressed!!'
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

if __name__=="__main__":
    main()

