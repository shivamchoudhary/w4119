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
    def printAll(self):
        members = [attr for attr in dir(Packet()) if not callable(attr) and not attr.startswith("__")]
        print members
    
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
"""
I created these functions while coding the first assignment so I am using it 
directly.
"""
def send_msg(sock, msg):
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)

def recv_msg(sock):
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    return recvall(sock, msglen)

def recvall(sock, n):
    data = ''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

