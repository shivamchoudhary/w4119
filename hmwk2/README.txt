TCP Protocol

NAME Simple TCP-like transport-layer protocol!!
        
DESCRIPTION:
TCP Segment structure:- According to RFC 793
##############################################################################
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
Sender Side FSM:-
##############################################################################
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
_______________________________________________________________________________
Receiver Side FSM:-
##############################################################################
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
_______________________________________________________________________________
INSTALLATION:The make file has some of the interesting options which help a lot
while testing. Just unzip the file and it should be good to go!!
OPTIONS:
Makefile Options:
lnkemu:- This will start the linkemulator with default BIT error rate of 1000
testsender:- Combine this when you are running with the linkemulator,it will 
pass the arguments to the link emulator port.
sender: This is for standalone operation with default port numbers specified
receiver: This is the only option for receiver with some defaults specified.
USAGE:
make receiver host the reciever on port 20000 and localhost.
make sender host the sender on port 20001 and localhost.
Last updated: 11/9/2015
