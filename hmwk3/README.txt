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
======================

*Desgined Protocol Structure: I use a json based protocol which has a key 'type',
which specifies the type of message. ROUTE_UPDATE,CLOSE can be the type of 
messages being sent to the other recievers. Alongwith that,the sends the current
Distance Vectors to the other neighbours.
=======================
- Has Autocomplete. If a partial command like sh is typed it will try to auto-
complete it for you.
*Usage Scenarios:-

*Protocol Specification:-
-> list of data messages used
-> semantics

*Additional Implementations
1) Can accept input in mixed format like Showrt,showrt etc
2) Can autocomplete the commands,provides rich help interface,seriously try it
3) If supplied with any argument in showrt <showrt 1>it will show the last 
time the route 
table was updated for a particular client.
4) Showneighbours : This command will show the neighbours and their current 
status
