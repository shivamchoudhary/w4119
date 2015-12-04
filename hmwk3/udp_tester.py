import socket
import time


def send():
    ip = '127.0.0.1'
    port = 4115
    msg = "First one"
    while True:
        time.sleep(3)
        sock  = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        sock.sendto(msg,(ip,port))
send()
