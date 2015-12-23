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
directive:
	python bfclient.py $(localport) $(timeout) $(ipaddress1) $(port1) $(weight1) $(ipaddress2) $(port2) $(weight2)
bfclient1:
	python bfclient.py $(localport) $(timeout) $(ipaddress1) $(port1) $(weight1) $(ipaddress2) $(port2) $(weight2)
bfclient2:
	python bfclient.py 4116 3 127.0.0.1 4115 5.0 127.0.0.1 4117 10.0 127.0.0.1 4118 5 
test:
	$(clean)
	gnome-terminal --window --maximize -e "tail -f client.log"
	python bfclient.py $(localport) $(timeout) $(ipaddress1) $(port1) $(weight1)
clean:
	rm *.pyc *.log 
