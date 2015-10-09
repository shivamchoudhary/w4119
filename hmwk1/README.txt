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

Configurations:-
config.json contains several variables which can be used to configure the 
global options for the server.
BLOCK_TIME : This changes the time a particular user is blocked from accessing 
the server after 'NUMFAILATT' login attempts.
NUMFAILATT : Changes the number of attempts wrong credentials are allowed.
host: The ip address on which the Server defaults.
Location: Specifies the location of the user_pass.txt file.
return_status: They specify the various return status for the messages recieved
from the Server.
The orgranization of code is in the following way:
1) Common.py:- 
>>It contains all the common functions used throughout by Server 
and Client. Also loads the json file ('config.json') and extracts users and 
password into the dictionary.
>> It has a recieve and send function which takes care of byte ordering and 
sends the size of the message len before sending it.
**Warning: Please make sure that the json is properly formatted before starting 
the server!! 
<==============================================================================>

Features:-
1)whoelse:- Shows the name of other client currently logged in
2)wholast <parameter> : Shows the other clients who have logged in that 
timeframe.
3)broadcast message <message>: Sends the message to all the connected user.It
might happen that you don't get ('$') symbol but its alright the client if 
executes the command will get the output without the prompt.
4)broadcast user <user1> <user2> <user3> message <message>: Sends the broadcast
to the users listed. It must have the word message else the commans will be
rejected by server.
5)message <user> <message> : Sends private message to the user. Again it might
look that the symbol('$') is not appearing but it alright the client is listening.
*6)adduser <username> <password> : Extra feature I have implemented, in the 
user_pass.txt you can specify a user whose name is admin. Now the userinfo.py has
an attribute admin which gets set on that name only. Hence the admin can add the
user. Since I was running short on time that user is able to login only after 
server restarts. The same can be verified by opening the file user_pass.txt
Eg:- adduser shivam shivam > will add the entry shivam shivam at the end of 
user_pass.txt
7)logout:- Logs out the particular user from the server.
