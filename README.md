# Subject

File transfer via TCP protocol. Handling exceptional situations by means of
the protocol.

# Description

## Client-server program for transferring files over a network using TCP

Implement a client and a serial server to allow file sharing. The server should
continue to support the commands that were implemented before, adding the file
transfer commands. The request to upload a file to (`UPLOAD`) or download from
(`DOWNLOAD`) the server should be initiated by the client. It is not necessary
to solve problems related to the fact that there is no such file, it is enough
to display a message that there is no file with the requested name.

Files must be transferred using TCP. The implementation must take into account
possible exceptional situations due to network problems, such as physical or
software connection failure.

The algorithm of connection break detection can be any, but such that the user
can find out about it in a reasonable time (from 30 seconds to 2–5 minutes).
The program should restore file transfer by itself before displaying a message
about connection problems. If the problem message is already displayed, it is
up to the user to decide whether to attempt recovery.

The server must support file download recovery, but with limitations: after
connection failure **the same client** has connected and is trying to download
**the same file** as in the previous session. If another client managed to
connect, or the server was restarted, the server has full right to delete
files related to incomplete downloads.

The server and the client are required to work within one thread.

## Study of out-of-band mode of data transfer

During data transfer via TCP, the transmitting side must generate out-of-band
data and display the total number of transmitted data bytes (not including
urgent bytes), the receiving side must display the total number of received
bytes (not including urgent bytes) when receiving urgent data.
