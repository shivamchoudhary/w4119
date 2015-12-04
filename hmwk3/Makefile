#BFCLIENT Parameters
localport :=4115 #Port number that the process should listen to.
timeout :=3 #Intertransmission time of ROUTE-UPDATE messages in steady state(seconds)

#other clients:
#@client 1
ipaddress1 :=127.0.0.1 #IP address of the neighbour,given in dotted decimal.
port1 :=4116 # The port number on which the neighbour is listening.
weight1 :=5.0 #A real number indicating the cost of the link.
#@client 2
ipaddress2:=127.0.0.1
port2:=4118
weight2:=30.0
#@many clients
#directives
bfclient:
	python bfclient.py $(localport) $(timeout) $(ipaddress1) $(port1) $(weight1)
bfclient2:
	python bfclient.py $(port1) $(timeout) 127.0.0.1 $(localport) $(weight1)
manyclient:
	python bfclient.py 4115 3 128.59.196.2 4116 5.0 128.59.196.2 4118 30.0
clean:
	rm *.pyc *.log 
