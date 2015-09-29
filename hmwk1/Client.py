import sys
import os
import socket

def connect(ip, port):
    try:
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (ip, port)
        serversocket.connect(server_address)
        while True:
            username  = raw_input("username:")
            serversocket.send(username)
            password  = raw_input("password:")
            serversocket.send(password)
    finally:
        pass

def main():
    try:
        ip = sys.argv[1]
        port = int(sys.argv[2])
    except IndexError:
        print "Please specify <server IP_address> <server_port_no>"
    connect(ip, port)
    
if __name__=="__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "Shutting Down the client!!"
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
