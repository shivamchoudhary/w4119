import sys
import socket
import Common
import struct
import os
import threading
import time
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
    make reciever   \
    (Without Proxy)  \
                      Without the Link Emulator  
    make sender      /
    make reciever   /
"""
timer_status = False
class Sender(object):

    def __init__(self, filename, remote_IP, remote_port, ack_port_num,
            log_filename, window_size):
        # Initializing Sender state command line variables.
        self.filename       = filename      #sent filename,default 'file.txt'
        self.remote_IP      = remote_IP     #IP for sending,default 127.0.0.1
        self.remote_port    = remote_port   #Port number 20000
        self.ack_port_num   = ack_port_num  #listening port,default 20001
        self.log_filename   = log_filename  #log file ,default send_logfile.txt
        self.window_size    = window_size   #window size,default 1152 bytes
        # Load file
        self.file           = open(self.filename)   #open the file to be sent.
        # Packet level
        self.MSS            = 2           #set maximum segment size to 576
        self.N              = self.MSS*self.window_size #set N to MSS*window
        self.InitialSeqNum  = 0
        self.NextSeqNum     = 1
        self.SendBase       = self.InitialSeqNum
        #Initialize the socket for udt_send
        self.udt_sock       = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,
                        socket.IPPROTO_UDP)
        self.udt_sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.filesize = os.stat(filename).st_size
        self.timerStatus = False
        self.udt_send()
    def udt_send(self):
        """
        Unreliably send the data through the channel!!
        """
        timer = Timer()
        while (self.NextSeqNum<self.filesize):
            if self.NextSeqNum < self.SendBase+self.N:
                pkt, length = self.make_pkt()
                self.send_data(pkt)
                self.NextSeqNum += length
                if not timer._start.isSet():
                    timer._start.set()
                    timer.start()
                
    def make_pkt(self):
        """
        Makes the packet
        return: packed packet and length of the message
        """
        self.file.seek(self.NextSeqNum -1)
        msg = self.file.read(self.MSS)
        pkt = Common.Packet(self.ack_port_num, self.remote_port, 
                self.NextSeqNum,0,msg)
        return pkt.pack(),len(msg)
    def send_data(self, pkt):
        """
        This just sends the packet over the link!!
        """
        self.udt_sock.sendto(pkt,(self.remote_IP,self.remote_port))
    def rdt_rcv(self):
        print "Hi"
        acksocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        acksocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) 
        try:
            acksocket.bind(('', self.ack_port_num))
        except socket.error as error:
            print ("Socket binding failed with error %s", error)
            sys.exit(0)
        acksocket.listen(5)
        print self.ack_port_num
        while True:
            (clientsocket,clientaddress) = acksocket.accept()
            print clientsocket
    def seekfile(self, seek_length=0):
        """
        Seeks the filename by window size,takes optional argument for 
        seeking
        """
        self.file.seek(seek_length)
        current_window = self.file.read(self.window_size)
        return current_window
def listener_thread():
    print "Listening"
    acksocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    acksocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) 
    try:
        acksocket.bind(('', 20001))
    except socket.error as error:
        print ("Socket binding failed with error %s", error)
        sys.exit(0)
    acksocket.listen(5)
    while True:
        (clientsocket,clientaddress) = acksocket.accept()
        print clientsocket
    acksocket.close()


class StoppableThread(threading.Thread):
    def __init__(self):
        super(StoppableThread, self).__init__()
        self._stop = threading.Event()
    def run(self):
        s = socket.socket()
        # s.settimeout(1)             # Socket will raise exception if nothing received
        s.bind(('127.0.0.1', 20001))
        s.listen(1)
        print("Listening on {}:{}".format(s.getsockname()[0], s.getsockname()[1]))
        while True:
            try:
                conn, addr = s.accept()
            except socket.error:
                # Check for stop signal
                if self._stop.is_set():
                    print("Shutting down cleanly...")
                    s.close()
                    return


class Timer(threading.Thread):
    """
    Subclassing Thread and setting a property as event
    Inspired from 
    https://mikeanthonywild.com/stopping-blocking-threads-in-python-using-
    gevent-sort-of.html
    """
    def __init__(self):
        super(Timer, self).__init__()
        self._start = threading.Event()
    def run(self):
        if self._start.is_set():
            time.sleep(1)
        else:
            return

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
