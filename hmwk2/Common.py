import struct
"""
Citations:
    1. Python struct Module 
    https://docs.python.org/2/library/struct.html

"""
class Packet(object):
    """
    Packets based on netinet/tcp.h header of Linux
    """
    def __init__(self,msg):
        self.sport  = 20000     #source port 16bit int
        self.dport  = 20000     #destination port 16bit int
        self.seq    = 0         #sequence number starts with 0 16 bit int
        self.ack    = 0         #Won't be used probably (simplex) 16 bit int
        self.off    = 0         #Data Offset (not used) 8 bit int
        self.flags  = 0         #Various flags (not used) 8 bit int
        self.win    = 0         #Window size(not used as no congestion control)
        self.sum    = 0         #Checksum computation 16 bit
        self.urp    = 0         #Urgent pointer not used
        self.msg    = msg
    def checksum(self, msg):
        """
        Computing the checksum taking two consequetive bits at a time. 
        """
        s = 0
        for i in range(0, len(msg), 2):
            w = (ord(msg[i]) << 8) + (ord(msg[i+1]) )
            s = s + w
            s = (s>>16) + (s & 0xffff);
            s = ~s & 0xffff
        return s
    def pack(self):
        """
        Creates the tcp_header with 20 bytes,then concatenates the packet with
        self.msg
        """
        tcp_header = struct.pack("!HHLLBBHHH", self.sport, self.dport, self.seq,
                self.ack, self.off, self.flags, self.win, self.sum, self.win)
        self.sum = self.checksum((tcp_header+self.msg))
        tcp_header = struct.pack("!HHLLBBHHH", self.sport, self.dport, self.seq,
                self.ack, self.off, self.flags, self.win, self.sum, self.win)
        packet = tcp_header+self.msg
        return packet

