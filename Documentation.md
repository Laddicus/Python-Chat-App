---
title: 'Documentation for Python Chat App'

header-includes:
 - \usepackage{fvextra}
 - \DefineVerbatimEnvironment{Highlighting}{Verbatim}{breaklines,commandchars=\\\{\}}
---

## RCF

### Authors and Date

Author: Devon Ladd
Started: Feb 3 2020
Handed in: April 9 2020

### Application name

Bad chat app

### Commands / Responses

Broadcast message:
Client would type something like `all:hello` or `ALL:How are you?`
Server sees the `broadcast` verb and passes the message along to all clients connected

Private message:
Client would type something like `Devon:hello`
Server sees the `PRIVATE_MESSAGE` verb and searches the dictionary for that names socket and then sends the message to that socket

Who:
Client would type `who` or `WHO`
Server sees the `WHO` verb and joins all values in the dictionary into a string and sends that message to the socket that sent the message

Login:
Client types there username and connects to the server
Server adds user to dictionary and sends a message to all clients telling them who has arrived

Quit:
Client types `quit` or `QUIT`
Server removes them from the dictionary and closes there socket

### Non-Command Verbs

Error message:
If the client receives an error message it merely prints the fact and continues on.

Resend request:
If the server receives a message with a packet that doesn't match the checksum
Sends a message with this verb to the client to request the resending of the last message

Confirm:
If the server receives a message with a packet that does match the checksum
Sends a message with this verb to the client to inform it that it does not need to resend the message

Shutdown:
When the server is being shutdown
Tells the client that the server is shutting down so it can stop listening to the server

### Packet

packet_number: integer

vn: integer

from_name: 32bit string

to_name: 32bit string

verb: integer

checksum: integer

encrypted: boolean

text: 256bit string

There are no separating characters

### Encryption

Rot13 but it also includes symbols (all ASCII characters from 32 - 126)

### LOG

Server:

```{.default}
[devonladd@loki Assignment4]$ python3 server.py
Checksums matched
From: devon, To: ALL, Contents: devon has connected., Verb: LOGIN
Checksums matched
From: not devon, To: ALL, Contents: not devon has connected., Verb: LOGIN
Checksums matched
From: devon, To: ALL, Contents: , Verb: WHO
devon, not devon
Checksums didn't match, requesting packet again...
Waiting...
Received...
Checksums matched
From: devon, To: all, Contents: uryy|, Verb: BROADCAST
Checksums didn't match, requesting packet again...
Waiting...
Received...
Checksums matched
From: not devon, To: devon, Contents: uv, Verb: PRIVATE_MESSAGE
devon: <socket.socket fd=4, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('192.197.151.116', 53289), raddr=('192.197.151.116', 47128)>
Checksums didn't match, requesting packet again...
Waiting...
Received...
Checksums matched
From: not devon, To: devon, Contents: u|%-n r-'|#-q|v{tL, Verb: PRIVATE_MESSAGE
devon: <socket.socket fd=4, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('192.197.151.116', 53289), raddr=('192.197.151.116', 47128)>
Checksums didn't match, requesting packet again...
Waiting...
Received...
Checksums matched
From: not devon, To: devon, Contents: y||x-n"-"uv!G-./0123i456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghiijklmnopqrstuvwxyz{|}~ !"#$%&'()*+,, Verb: PRIVATE_MESSAGE
devon: <socket.socket fd=4, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('192.197.151.116', 53289), raddr=('192.197.151.116', 47128)>
Checksums matched
From: not devon, To: ALL, Contents: not devon has disconnected., Verb: QUIT
not devon disconnected.

Sending disconnect message to ALL
DISCONNECTED
No longer listening to <socket.socket [closed] fd=-1, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0>
Checksums matched
From: devon, To: ALL, Contents: , Verb: WHO
devon
Checksums matched
From: also not devon, To: ALL, Contents: also not devon has connected., Verb: LOGIN
Checksums didn't match, requesting packet again...
Waiting...
Received...
Checksums matched
From: also not devon, To: all, Contents: uv, Verb: BROADCAST
Checksums matched
From: also not devon, To: ALL, Contents: also not devon has disconnected., Verb: QUIT
also not devon disconnected.

Sending disconnect message to ALL
DISCONNECTED
No longer listening to <socket.socket [closed] fd=-1, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0>
Checksums matched
From: devon, To: ALL, Contents: devon has disconnected., Verb: QUIT
devon disconnected.

DISCONNECTED
No longer listening to <socket.socket [closed] fd=-1, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0>
^CMessaging all clients...
Closing all sockets...
Done. Goodbye.
```

Client 1 (devon):

```{.default}
[devonladd@loki Assignment4]$ python3 client.py
Username: devon
Connected
Message confirmed

devon has connected.


not devon has connected.

who
Message confirmed

devon, not devon

all:hello
Message from will have the wrong checksum
Message confirmed

TO: all
FROM: devon
hello


TO: devon
FROM: not devon
hi


TO: devon
FROM: not devon
how are you doing?


TO: devon
FROM: not devon
look at this: !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~


not devon has disconnected.

who
Message confirmed

devon


also not devon has connected.


TO: all
FROM: also not devon
hi


also not devon has disconnected.

bye
See ya
```

Client 2 (not devon):

```.{default}
[devonladd@loki Assignment4]$ python3 client.py
Username: not devon
Message confirmed
Connected

not devon has connected.


TO: all
FROM: devon
hello

devon:hi
Message from will have the wrong checksum
Message confirmed

TO: devon
FROM: not devon
hi

devon:how are you doing?
Message from will have the wrong checksum
Message confirmed

TO: devon
FROM: not devon
how are you doing?

devon:look at this: !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~
Message from will have the wrong checksum
Message confirmed

TO: devon
FROM: not devon
look at this: !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~

bye
See ya
```

Client 3 (also not devon):

```.{default}
[devonladd@loki Assignment4]$ python3 client.py
Username: also not devon
Message confirmed
Connected

also not devon has connected.

all:hi
Message from will have the wrong checksum
Message confirmed

TO: all
FROM: also not devon
hi

bye
See ya
```
