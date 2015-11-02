import sys

class Receiver(object):
    def __init__(self, filename, listening_port, sender_IP, sender_port,
            log_filename_receiver):
        """
        Initializing the Receiver Object with all the parameters.
        """
        self.filename = filename
        self.listening_port = listening_port
        self.sender_IP = sender_IP
        self.sender_port = sender_port
        self.log_filename_receiver = log_filename_receiver


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
        Receiver(filename, listening_port, sender_IP, sender_port,
                log_filename_receiver)
    except IndexError:
        print "Some parameter(s) is/are missing invoke in the following format",\
                "<filename> <listening_port> <sender_IP> <sender_port> ",\
                "<log_filename_receiver>"


if __name__ =="__main__":
    main()
