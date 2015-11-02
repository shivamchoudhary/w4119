import sys

class Sender(object):

    def __init__(self, filename, remote_IP, remote_port, ack_port_num,
            log_filename, window_size):
        '''Initializing the Sender Object with all the parameters'''
        self.filename = filename #the filename to be sent default file.txt
        self.remote_IP = remote_IP #IP for sending,default 127.0.0.1
        self.remote_port = remote_port #Port number default 20000
        self.ack_port_num = ack_port_num #listening port default 20001
        self.log_filename = log_filename #log filename default send_logfile.txt
        self.window_size = window_size #window size default 1152 bytes
        
        #other default settings:
        self.file = open(self.filename) #open the file to be sent.
        self.seekfile()
    def seekfile(self, seek_length=0):
        '''seeks the filename by window size,takes optional argument for 
        seeking'''
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
        Sender(filename,remote_IP,remote_port,ack_port_num,log_filename,window_size)
    except IndexError:
        print "python sender.py <filename> <remote_IP> <remote_port>",\
        "<ack_port_num> <log_filename> <window_size>" 
        sys.exit(2)

if __name__=="__main__":
    main()

