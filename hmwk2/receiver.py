import sys

class receiver(object):
    def __init__(self):
        pass



def main():
    try:
        filename = str(sys.argv[1]) 
        listening_port = int(sys.argv[2])
        sender_IP = int (sys.argv[3])
        sender_port = int(sys.argv[4])
        log_filename_receiver = str(sys.argv[5])
    except IndexError:
        print "Some parameter(s) is/are missing invoke in the following format",\
                "<filename> <listening_port> <sender_IP> <sender_port> ",\
                "<log_filename_receiver>"
