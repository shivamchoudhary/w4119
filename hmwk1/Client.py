import sys
import os







def main():
    print "Main"
    try:
        ip = int(sys.argv[1])
        port = int(sys.argv[2])
    except IndexError:
        print "Please specify <server IP_address> <server_port_no>"
    print (port,ip)
    
if __name__=="__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "Shutting Down the client!!"
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
