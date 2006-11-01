import socket
import sys
import string
import gtk
import time
from gazpacho.loader.loader import ObjectBuilder
from threading import Thread

if len(sys.argv) !=  3: 
        print 'Usage Server.py HOST PORT'
        sys.exit(0)    
else:
    HOST,PORT  = sys.argv[1:3]
    print 'Start Server on ip '+ HOST+' on PORT '+PORT



wt = ObjectBuilder('Servidor.glade')
wt.signal_autoconnect(globals())
wt.toplevels[0].show_all()
buffer = gtk.TextBuffer()
textview1 = wt.get_widget('textview1')


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((HOST, string.atoi(PORT)))

serversocket.listen(2)
clientsocket = None

class Escuta(Thread):
    def run(self):
        go = True
        #(clientsocket, address) = serversocket.accept()

        while go:
            time.sleep(1)
            data = clientsocket.recv(1024)
            #repr(data)
            if data == "shutdown":
                go=False
                #sys.exit(0)
            else:
                
                #buffer = textview1.get_buffer()
                print data
                buffer.set_text(data +'\n',False)
                textview1.set_buffer(buffer)    
        
#Escuta().start()
def escreve(sock,cond):
    print 'foi'
    clientsocket = sock
    Escuta().start()
    return False
id = gtk.input_add(serversocket, gtk.gdk.INPUT_READ, escreve)        
gtk.main()
