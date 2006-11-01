import socket
import sys
import string

 

if len(sys.argv) !=  3: 
        print 'Usage Server.py HOST PORT'
        sys.exit(0)    
else:
    HOST,PORT  = sys.argv[1:3]
    print 'Start Server on ip '+ HOST+' on PORT '+PORT


l=[]
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((HOST, string.atoi(PORT)))
serversocket.listen(1)

while 1:
    (clientsocket, address) = serversocket.accept()
    data = clientsocket.recv(1024)
    repr(data)
    if data == "shutdown":
        sys.exit(0)
    else:
        l.append(data)
        print l

    

        