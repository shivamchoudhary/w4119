Distributed Bellman-Ford
=====================

*How to Run:-
- make bfclient1 
- make bfclient2
in two separate terminals would load the scenario as given in the specifications.
=====================

* Supported Commands:-
All commands specified are supported,alogwith the following extra commands:-
- showneighbours: This command will show the neighbours of the current client 
alongwith the last_updated values.
=====================

*Project Documentation:-
Makefile:- The included makefile can provide direct command line interface to 
run the program directly as specified in the How to Run section.
Common.py :- Contains all the Common Functions like Sender Socket and Receiver
Socket
bfclient.py :- Contains the Command Line Interface and thread inits.
=======================
*Usage Scenarios:-

Accepts input in command line format. Also one neighbour has to be supplied for 
init,else error will be raised.
Any number of client can be inited and if they don't have 3 tuples error will 
be raised.
========================
*Protocol Specification:-
*Desgined Protocol Structure: I use a json based protocol which has a key 'type',
which specifies the type of message. ROUTE_UPDATE,CLOSE can be the type of 
messages being sent to the other recievers. Alongwith that,the sends the current
Distance Vectors to the other neighbours.

-> list of data messages used
ROUTE_UPDATE, CLOSE,LINK_UP,LINK_DOWN
-> semantics
The message that is sent out has the following format:-
message = {
        'ip':'127.0.0.1',
        'port':4116,
        'link':'127.0.0.1:4116',
        'cost':'5',
        'dvtable':{
            '127.0.0.1:4115':{
                "cost":5,
                "ip":'127.0.0.1',
                "port":4115,
                },
            '127.0.0.1:4118':{
                "cost":5,
                "ip":"127.0.0.1",
                "port":4118,
                },
            '127.0.0.1:4117':{
                "cost":10,
                "ip":"127.0.0.1",
                "port":4117,
                }

            }
        }


*Additional Implementations
1) Can accept input in mixed format like Showrt,showrt etc
2) Autocomplete the commands,provides rich help interface,seriously try it 
3) Showneighbours : This command will show the neighbours and their current 
status with last updated values.
