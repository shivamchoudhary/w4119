import json

def read_config(fname = "config.json"):
    with open("config.json") as conf:
        configuration = json.load(conf)
    return configuration

