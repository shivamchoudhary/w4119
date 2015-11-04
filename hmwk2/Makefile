#Common Parameters
filename := test.txt #common for both reciever and sender

#Reciever Parameters
listening_port :=20000
sender_IP :=127.0.0.1
sender_port :=20001
log_filename_receiver :=recv_logfile.txt

#Sender Parameters
remote_IP :=127.0.0.1
remote_port :=20000
ack_port_num :=20001
log_filename_sender :=send_logfile.txt
window_size :=1152

#Testing with link emulator
lnkemu_port :=41192

sender:
	python sender.py $(filename) $(remote_IP) $(remote_port) $(ack_port_num)  $(log_filename_sender) $(window_size)

reciever:
	python receiver.py $(filename) $(listening_port) $(sender_IP) $(sender_port) $(log_filename_receiver)

lnkemu:
	./newudpl -i 127.0.0.1:* -o 127.0.0.1:$(remote_port) -B 1000 -vv

testsender:
	python sender.py $(filename) $(remote_IP) $(lnkemu_port) $(ack_port_num)  $(log_filename_sender) $(window_size)

clean:
	rm *.pyc logfile.txt
