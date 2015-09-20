import json

def read_config(fname = "config.json"):
    with open("config.json") as conf:
        configuration = json.load(conf)
    return configuration

def load_password(fname):
    user_passdict = {}
    with open(fname) as userpassf:
        userpassf  = userpassf.read().splitlines()
        for val in userpassf:
            vals = val.split(" ")
            print vals[0]

        return user_passdict



load_password('user_pass.txt')
