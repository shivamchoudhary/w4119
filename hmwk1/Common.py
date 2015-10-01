"""
Set of generic functions used throughout the Server/Client.
"""
import json
import struct


def read_config(fname = "config.json"):
    """
    Reads the config.json and returns the full key-value pairs.
    """
    with open("config.json") as conf:
        configuration = json.load(conf)
    return configuration

def load_password(fname):
    """
    Loads the user_pass.txt file and splits the username and password
    fname:name of the file from which it has to read.
    user_passdict:A key-value pair of username and password.
    usernames: An array of registered usernames.
    """
    userpass_dict = {}
    usernames = []
    with open(fname) as userpassf:
        userpassf  = userpassf.read().splitlines()
        for val in userpassf:
            vals = val.split(" ")
            userpass_dict[vals[0]] = vals[1]
            usernames.append(vals[0])
        print userpass_dict,usernames
        return userpass_dict, usernames

"""
The following code is abstracted from the following reference. 
The reason was I was not getting the length of the string which made it annoying.
Reference: http://stackoverflow.com/questions/17667903/\
python-socket-receive-large-amount-of-data    
"""
"""
These are the generic library functions for sending and recieving the data.
"""

def send_msg(sock, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)

def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(sock, msglen)

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = ''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data
