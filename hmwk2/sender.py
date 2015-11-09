import sys
import socket
import Common
import struct
import os
import threading
import time
import select
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
        self.fin            = 0
        #Initialize the socket for udt_send
        self.udt_sock       = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,
                        socket.IPPROTO_UDP)
        self.udt_sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.filesize = os.stat(filename).st_size
        #
        self.acksocket_initial = False
        self.numpackets = int(self.filesize/self.MSS)+(self.filesize%self.MSS>0)
        #sender stats:-
        self.udt_send()
    
    def udt_send(self):
        """
        Unreliably send the data through the channel!!
        """
        self.acksocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.acksocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        connected = False
        try:
            self.acksocket.bind(('localhost',self.ack_port_num))
        except socket.error as e:
            print "Socket Error %s"%e
        self.acksocket.listen(6)
        EstimatedRTT = 2
        numpackets = 0
        stats = Stats()
        while (self.NextSeqNum<self.filesize):
            numpackets+=1
            if numpackets ==self.numpackets:
                self.fin = 1
            TimeoutInterval = RTT()
            TimeoutInterval = TimeoutInterval.update(EstimatedRTT)
            pkt, length = self.make_pkt()
            self.send_data(pkt)
            send_time = time.time()
            self.NextSeqNum += length
            stats.updateTotalBytesSent(int(length))
            stats.updateSegmentsSent()
            if not connected:
                clientsocket,clientaddress = self.acksocket.accept()
                connected = True
            while True:
                r,a,b = select.select([clientsocket],[],[],TimeoutInterval)
                if r:
                    data = clientsocket.recv(1024)
                    print data
                    EstimatedRTT = time.time()-send_time
                    break
                if not r:
                    print "Timeout"
                    self.send_data(pkt)
                    stats.updateTotalBytesSent(int(length))
                    stats.updateSegmentsSent()
                    stats.updateSegmentsRestransmitted()
        stats.printStats()
    def make_pkt(self):
        """
        Makes the packet
        return: packed packet and length of the message
        """
        self.file.seek(self.NextSeqNum -1)
        msg = self.file.read(self.MSS)
        pkt = Common.Packet(self.ack_port_num, self.remote_port, 
                self.NextSeqNum,self.fin,msg)
        return pkt.pack(),len(msg)
    
    def send_data(self, pkt):
        """
        This just sends the packet over the link!!
        """
        self.udt_sock.sendto(pkt,(self.remote_IP,self.remote_port))
    
    def seekfile(self, seek_length=0):
        """
        Seeks the filename by window size,takes optional argument for 
        seeking
        """
        self.file.seek(seek_length)
        current_window = self.file.read(self.window_size)
        return current_window
    def ack_rcv(self):
        while True:
            (clientsocket, clientaddress) = self.acksocket.accept()
            data = clientsocket.recv(1024)
            if data:
                print data
            # clientsocket.close()
            break


class Stats():
    def __init__(self):
        self.TotalBytesSent = 0
        self.SegmentsSent = 0
        self.SegmentsRetransmitted = 0
    def updateTotalBytesSent(self,length):
        self.TotalBytesSent+=length
    def updateSegmentsSent(self):
        self.SegmentsSent+=1
    def updateSegmentsRestransmitted(self):
        self.SegmentsRetransmitted+=1
    def printStats(self):
        print "Delivery completed successfully"
        print "Total bytes sent = %s" %self.TotalBytesSent
        print "Segments sent = %s" %self.SegmentsSent
        print "Segments retransmitted = %s" %self.SegmentsRetransmitted

class RTT():
    """
    Keeps track of RTT,
    """
    def __init__(self):
        """
        Init all vals except Estimated RTT
        """
        self.SampleRTT = 2
        self.DevRTT = 0
        self.TimeoutInterval =1
    def update(self,EstimatedRTT):
        """
        param EstimatedRTT: The difference between send_packet time and 
        recieving the acks
        """
        EstimatedRTT = (0.875)*EstimatedRTT + 0.125*self.SampleRTT
        self.DevRTT = 0.75*self.DevRTT +0.25*(self.SampleRTT-EstimatedRTT)
        self.TimeoutInterval = EstimatedRTT +4*self.DevRTT
        return self.TimeoutInterval

class StoppableThread(threading.Thread):
    def __init__(self):
        super(StoppableThread, self).__init__()
        self._stop = threading.Event()
    def run(self):
        s = socket.socket()
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

class recvAcks(threading.Thread):
    def __init__(self):
        super (recvAcks,self).__init__()
        self._start = threading.Event()
        self._stop = threading.Event()
    
    def run(self):
        server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        server.bind(('localhost', 20001))
        server.listen(5)
        if self._start.isSet():
            print "Listening for ACKS",time.time()
            client,addr  = server.accept()
            while True:
                # client,addr = server.accept()
                try:
                    data = client.recv(1024)
                    if data:
                        print data
                except socket.error:
                    if self._stop.isSet():
                        print "Graceful Shutdown"
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
        # t1 = recvAcks()
        # t1._start.set()
        # t1.deamon = True
        # t1.start()
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
            t1._stop.set()
        except SystemExit:
            os._exit(0)

if __name__=="__main__":
    main()
