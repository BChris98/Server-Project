from peertopeer import *
from clientserv import *
import socket
import re

class Intro :
    def __init__ (self):

        print ("Souhaitez vous vous connectez à un serveur(1), à une machine(2) ou héberger un serveur(3)")
        choix = int(input())
        liste = [1,2,3]
        if choix not in liste:
            print ("Erreur dans l'exécution de la commande")
            self.__init__()

        if choix == 1:
            self.server()
        elif choix == 2:
            self.machine()
        else:
            self.heberge()
    def server (self):

        print ("Identifiez-vous avec un pseudo")
        pseudo = str(input())
        if pseudo == '':
            print ("Erreur dans l'encodage du pseudo")
            self.server ()

        print ("Quel est l'adresse ip du serveur sur lequel vous souhaitez vous connectez ?")
        ip = str(input())
        pattern = r"(\d{1,3}.){3}\d{1,3}"
        p = re.compile (pattern)
        if p.match (ip) is None:
            print ("Erreur dans l'encodage de l'adresse ip")
            self.server()
        try:
            print ("Et le port de connection ?")
            port = int(input())
        except:
            print ("Erreur dans l'encodage du port")
            self.server()
            
        adress = (ip,port)
        Client(adress,pseudo).run()
    
    def machine (self):
        
        try:
            print("Sous quel port souhaitez vous écouter ?")
            port = int(input())
        except:
            print ("Erreur dans l'encodage du port")
            self.machine()

        Chat(socket.gethostname(),port).run()

    def heberge (self):

        try:
            print ("Sur quel port souhaitez vous héberger votre serveur?")
            port = int(input())
        except:
            print ("Erreur dans l'encodage du port")
            self.heberge()

        adress = (socket.gethostname(), port)
        Server(adress).run()

if __name__ == '__main__':
    Intro()