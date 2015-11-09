import struct
import time
"""
Citations:
    1. Python struct Module 
    https://docs.python.org/2/library/struct.html

"""
class Packet(object):
    """
    Packets based on netinet/tcp.h header of Linux
    """
    def __init__(self, ack_port_num, remote_port, seq, fin,msg):
        self.sport  = ack_port_num     #source port 16bit int
        self.dport  = int(remote_port)   #destination port 16bit int
        self.seq    = int(seq)         #sequence number starts with 0 16 bit int
        self.ack    = 0             #Won't be used probably (simplex) 16 bit int
        self.off    = 0             #Data Offset (not used) 8 bit int
        ###############             #TCP_FLAGS only FIN is used
        self.FIN    = fin           #Set to 1 if last packet 
        self.SYN    = 0
        self.RST    = 0
        self.PUSH   = 0
        self.ACK    = 0
        self.URG    = 0
        ###############
        self.win    = 0             #Window size(not used no congestion control)
        self.sum    = 0             #Checksum computation 16 bit
        self.urp    = 0             #Urgent pointer(not used)
        self.msg    = msg
    def pack(self):
        """
        Creates the tcp_header with 20 bytes,then concatenates the packet with
        self.msg
        """
        self.flags = self.FIN+(self.SYN<<1)+(self.RST<<2)+(self.PUSH<<3)+\
                    (self.ACK<<4) +(self.URG<<5)
        tcp_header = struct.pack("!HHLLBBHHH", self.sport, self.dport, self.seq,
                self.ack, self.off, self.flags, self.win, self.sum, self.win)
        self.sum = checksum((tcp_header+self.msg))
        tcp_header = struct.pack("!HHLLBBHHH", self.sport, self.dport, self.seq,
                self.ack, self.off, self.flags, self.win, self.sum, self.win)

        packet = tcp_header+self.msg
        return packet
class log(object):
    
    def __init__(self, source, destination, logging_method, 
            EstimatedRTT_bit = False):
        self.source = source
        self.destination = destination
        self.fin = 0
        self.logging_method = logging_method
        self.EstimatedRTT_bit = EstimatedRTT_bit
    def sequence(self, Sequence):
        self.Sequence = Sequence
        self.Sequence = "Sequence "+str(self.Sequence) 
    def ack(self, ACK):
        self.ACK = ACK
        self.ACK = "ACK " +str(self.ACK) 
    def EstimatedRTT(self,EstimatedRTT):
        self.estimate = EstimatedRTT
        self.estimate = "EST_RTT "+str(self.estimate)
    def write(self,f=None):
        logline = str(time.time())+" "+"Source "+str(self.source)+" "+"Destination" +" "+str(self.destination)+" "+str(self.Sequence)+" "+str(self.ACK)+" "+"Fin "+str(self.fin)
        if self.EstimatedRTT_bit:
            logline = str(logline)+" "+str(self.estimate)
        if self.logging_method:
            f.write(format(logline))
            f.write("\n")
        else:
            print logline
def checksum(msg):
        """
        Computing the checksum taking two consequetive bits at a time.
        staticmethod to be used by reciever as well
        """
        s = 0
        for i in range(0, len(msg), 2):
            w = (ord(msg[i]) << 8) + (ord(msg[i+1]) )
            s = s + w
            s = (s>>16) + (s & 0xffff);
            s = ~s & 0xffff
        return s

