"""
Set of generic functions used throughout the Server/Client.
"""
import json
import struct
import pickle

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
        return userpass_dict, usernames
def add_user(fname,username,password):
    cred = username+" "+password
    with open(fname,"a") as userpassf:
        userpassf.write(cred)

def close_socket(sock):
    sock.shutdown(1)
    sock.close()


"""
These are the generic library functions for sending and recieving the data.
"""

def send_msg(sock, msg):
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)

def recv_msg(sock):
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    return recvall(sock, msglen)

def recvall(sock, n):
    data = ''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

