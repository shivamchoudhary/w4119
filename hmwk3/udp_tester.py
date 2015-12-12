import socket
import time
import json
def send(msg):
    ip = '127.0.0.1'
    port = 4115
    sock  = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.sendto(msg,(ip,port))
class Message(object):
    """ 
    Messages exchanged between the clients. Each has data type.
    ROUTE_UPDATE    :(ip,port,dv) tuple
    LINK_UP         :(ip,port,dv)
    LINK_DOWN       :(ip,port)
    """
    ROUTE_UPDATE,LINK_UP,LINK_DOWN = range(3)
    def __init__(self, type, data=None):
        self.type = type
        self.data = data

class Handlers(object):
    
    def __init__(self,q):
        self.handlers = {
                Message.ROUTE_UPDATE:self._route_UPDATE
                }
        self.q = q
        self.run()
    def run(self):
        cmd = self.q
        self.handlers[cmd.type](cmd)

    def _route_UPDATE(self, msg):
        data = json.dumps(msg.data)
        send(data)
message = {'testing':"hh"}
Handlers(Message(Message.ROUTE_UPDATE,message))
# send()
