TCP Protocol

NAME Simple TCP-like transport-layer protocol!!
        
*DESCRIPTION:

1)TCP Segment structure:- According to RFC 793

0                   1                   2                   3   
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |          Source Port          |       Destination Port        |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |Sequence Number(starts from zero increment in length of MSG)   |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |          Acknowledgment Number(Not used)                      |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |  Data |           |0|s|0|0|0|0|                               |
   | Offset| Reserved  |0|e|0|0|0|0|            Window(Not used)   |
   |       |           |0|q|0|0|0|1|FIN only Last time             |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |          Checksum(data+header)|Urgent Pointer(Not used)       |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                    Options(Not used)          |Notused        |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                             data                              |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+


2)Sender Side FSM:-
Initialize:
    N = window_size * MSS
    InitialSeqNum = 0
    NextSeqNum = 1
    SendBase = InitialSeqNum
event:udt_send
    if NextSeqNum <SendBase +N:
        pkt = make_pkt(data)
        send_data(pkt)
        if (timer not running):
            start_timer
        NextSeqNum +=len(data)
event:timeout:
    retransmit from send_base
    start_timer
event: ACK recieved:
    if y>SendBase:
        SendBase=y
        if no currently unack seg:
            start timer


3)Receiver Side FSM:-
Initialize:
    ExpectedSeqNumber = 1
event:recv_data and finnotset
    if x==ExpectedSeqNumber:
        write_to_file
        send_ack(ExpectedSeqNumber+len(data))
        ExpectedSeqNumber+=len(data)
event:FIN BIT set:
    write_to_file
    send_ack()


4) Loss Recovery Mechanism:-
The sender after sending a packet updates its TIMEOUT variable and if it doesn't
get the ACK back in that timeout it sends the packet again.
The reciever if receives a packet which has different seqnumber from what it 
expects it just drops it else it writes into the file.


5) Assumptions:-
Sample RTT = 2
MSS = 576 bytes
Initial Timeout  = 1(Though it gets updated in the first round itself)
_______________________________________________________________________________
*INSTALLATION:

The make file has some of the interesting options which help a lot
while testing. Look into some of the Makefile Options
_______________________________________________________________________________

*OPTIONS:

1)Makefile Options:
*make lnkemu:- This will start the linkemulator with default BIT error rate 
of 1000.
*make testsender:- Combine this when you are running with the linkemulator,it 
will pass the arguments to the link emulator port. By default logging on stdout.
*make sender: This is for standalone operation with default port numbers 
specified,by default logging on stdout.
*make receiver: This is the only option for receiver with some defaults 
specified,by default logging on stdout.
_______________________________________________________________________________

*USAGE:
1)make receiver host the reciever on port 20000 and localhost logs on stdout.
2)make sender host the sender on port 20001 and localhost logs on stdout.
_______________________________________________________________________________

*Known Limitations:
1)Sometimes when the first checksum fails when it is sent throught linkemulator
it gets stuck and does not move forward. It's weird because when I try to delay
the ack deliberately from reciever side(without linkemulator) it works properly.
I am unable to debug this issue partly due to time constraints and due to 
unfamiliarity with newudpl code base. Well as of now I can only ask that you 
restart the reciever and sender again till the first packet passes the checksum.

2)Referring https://piazza.com/class/ie5l0ldfg5c6y6?cid=175. I have seen the 
proxy to crash when it is overwhelmed with packets. This is not reproducible 
consistenly if the packets are sent one by one. 
_______________________________________________________________________________
Last updated: 11/9/2015
