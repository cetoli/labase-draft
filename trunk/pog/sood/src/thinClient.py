import socket
import string
import sys


class SoodClient:
       
        def __init__(self,sock = None):
            if sock is None:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            else:
                self.sock = sock

        def Connecta(self,HOST,PORT):
            self.sock.connect((HOST,string.atoi(PORT)))
            
            
        def EnviarMSG(self,DATA):
            self.sock.send(DATA)
           
            
        def Fechar(self):
            self.sock.close()




    

