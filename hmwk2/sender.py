import sys
import socket
import Common
import struct
import os
"""
Citations:
"""
"""
Sender FSM:-
1)Architecture as per assignment:-
            Proxy(port 41192)
              /       \                
          sender    receiver
       (127.0.0.1) (127.0.0.1)
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
        """
        Initializing the Sender state.
        """
        self.filename       = filename      #sent filename,default 'file.txt'
        self.remote_IP      = remote_IP     #IP for sending,default 127.0.0.1
        self.remote_port    = remote_port   #Port number
        self.ack_port_num   = ack_port_num  #listening port,default 20001
        self.log_filename   = log_filename  #log file ,default send_logfile.txt
        self.window_size    = window_size   #window size,default 1152 bytes
        # Load file
        self.file   = open(self.filename) #open the file to be sent.
        window      = self.seekfile()
        send_sock        = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,
                        socket.IPPROTO_UDP)
        packet          = Common.Packet(window)
        data            = packet.pack()
        send_sock.sendto(data,(self.remote_IP,self.remote_port))
    
    def rdt_send(self,data):
        """
        Reliably recieve data,send over unreliable channel.
        """
        pass

    def timeout(self):
        pass
    def rdt_rcv(self):
        pass 
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
        print 'ctrl-c pressed!!'
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

if __name__=="__main__":
    main()

