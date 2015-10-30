import sys

class Sender(object):
    def __init__(self,filename,remote_IP,remote_port,ack_port_num,log_filename,
            window_size):
        self.filename = filename
        self.remote_IP = remote_IP
        self.remote_port = remote_port
        self.ack_port_num = ack_port_num
        self.log_filename = log_filename
        self.window_size = window_size

def main():
    try:
        filename        = str(sys.argv[1])
        remote_IP       = sys.argv[2]
        remote_port     = int(sys.argv[3])
        ack_port_num    = int(sys.argv[4])
        log_filename    = str(sys.argv[5])
        window_size     = int(sys.argv[6])
    except IndexError:
        print "python sender.py <filename> <remote_IP> <remote_port>",\
        "<ack_port_num> <log_filename> <window_size>" 
        sys.exit(2)



if __name__=="__main__":
    main()

