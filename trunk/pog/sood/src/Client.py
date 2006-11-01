import socket
import string
import sys
import gtk
from gazpacho.loader.loader import ObjectBuilder

if len(sys.argv) != 4 : 
        print 'Usage Client.py HOST PORT DATA'
        sys.exit(0)    
else:
    HOST,PORT,DATA  = sys.argv[1:4]
    print 'Connect client on ip '+ HOST+' on PORT '+PORT

HOST,PORT,DATA  = sys.argv[1:4]




class SoodClient:
       
        def __init__(self,sock = None):
            self.wt = ObjectBuilder('Client.glade')
            wt = self.wt
            wt.signal_autoconnect(globals())
            wt.toplevels[0].show_all()
            self.buffer = gtk.TextBuffer()
            self.entry1 = wt.get_widget('entry1')        
            button1 = wt.get_widget('button1')        
            button2 = wt.get_widget('button2')        
            dic = { "on_button1_clicked" : \
                     self.button1_clicked, "on_serverinfo_destroy" : \
                     (gtk.mainquit) }
            self.wt.signal_autoconnect (dic)
            if sock is None:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            else:
                self.sock = sock

        def button1_clicked(self,widget):
            data = 'oioi'
            #self.buffer.set_text(data +'\n',False)
            data = self.entry1.get_text()
            print data
            
            self.EnviarMSG(data)
        def Connecta(self,HOST,PORT):
            self.sock.connect((HOST,string.atoi(PORT)))
            
            
        def EnviarMSG(self,DATA):
            self.sock.send(DATA)
           
            
        def Fechar(self):
            self.sock.close()




if __name__ == '__main__':
    chat = SoodClient()
    chat.wt.toplevels[0].show_all()
    chat.Connecta(HOST,PORT)
    gtk.main()

wt.get_widget('textview1') 