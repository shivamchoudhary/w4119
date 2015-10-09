Homework 1: Computer Networks
Shivam Choudhary(sc3973)

<==============================================================================>
Instructions For Running the code:-
1) Auto Mode:-
* There is a make file with two directives server and client
>> make server (This will bind the server on the localhost and port 4119)
>> make client (This will attach the client to the localhost and port 4119)
2) Manual Mode:-
python Server.py <port-number>
python Client.py <server-ip-address> <server-port-number>
<==============================================================================>
<==============================================================================>
Configurations:-
config.json contains several variables which can be used to configure the global options for the server.
BLOCK_TIME : This changes the time a particular user is blocked from accessing 
the server after 'NUMFAILATT' login attempts.
NUMFAILATT : Changes the number of attempts wrong credentials are allowed.
host: The ip address on which the Server defaults.
Location: Specifies the location of the user_pass.txt file.
return_status: They specify the various return status for the messages recieved
from the Server.
<==============================================================================>


