import socket
import sys
import threading
import re

class Server:
    def __init__(self,SERVERADDRESS):
        self.__adr = SERVERADDRESS
        self.__s = socket.socket()
        self.__s.bind(self.__adr)
        self.__client = [socket.gethostname()]
        try:
            with open ("pseudo.txt","w") as file:
                file.write ("admin")
                file.write("\n")
        
        except:
            print ("Erreur dans l'ouverture de la base de données")
            
    def run(self):
        self.__s.listen()
        while True:

            client, addr = self.__s.accept()
            try:
                with open ("pseudo.txt","r") as file:
                    pseudos = file.readlines ()
            except:
                print ("Erreur dans l'ouverture de la base de données")

            if len(pseudos) > len(self.__client):
                self.__client.append (addr[0])

            try:
                recu = self._receive(client).decode()
                p = re.compile ("(?P<pseudo>.+)(?P<residu>\\n)")

                if recu == "clientlist":
                    liste_client = []

                    for i in range (0,len(pseudos)):
                        m = p.match (pseudos[i])
                        liste_client.append ((self.__client[i],m.group("pseudo")))

                    print ("Les utilisateurs connectés sont :")
                    for i in liste_client:
                        print ("{} : {}".format(i[1],i[0]))

                else:
                    place = self.__client.index(addr[0])
                    m2 = p.match (pseudos[place])
                    print("{} : {}".format(m2.group("pseudo"),recu))

                client.close()

            except OSError:
                print('Erreur lors de la réception du message.')

    def _receive(self, client):
        chunks = []
        finished = False
        while not finished:
            data = client.recv(1024)
            chunks.append(data)
            finished = data == b''
        return b''.join(chunks)


class Client:
    def __init__(self, SERVERADDRESS,pseudo):
        self.__adr = SERVERADDRESS
        self.__pseudo = pseudo
        try:
            with open ("pseudo.txt","a") as file:
                file.write (self.__pseudo)
                file.write("\n")
        except:
            print ("Erreur dans l'ouverture de la base de données")

    def run(self):
        handlers = {
            '/send': self._send,
            '/client': self._client
        }
        self.__running = True
        self.__address = None
        print ("/send","/client")
        while self.__running:
            line = sys.stdin.readline().rstrip() + ' '
            # Extract the command and the param
            command = line[:line.index(' ')]
            param = line[line.index(' ') + 1:].rstrip()
            # Call the command handler
            if command in handlers:
                try:
                    handlers[command]() if param == '' else handlers[command](param)
                except:
                    print("Erreur lors de l'exécution de la commande.")
            else:
                print('Command inconnue:', command)
    
    def _send(self,message):
        try:
            self.__s = socket.socket()
            self.__s.connect(self.__adr)
            totalsent = 0
            msg = message
            try:
                while totalsent < len(msg):
                    sent = self.__s.send(msg[totalsent:].encode())
                    totalsent += sent
            except OSError:
                print("Erreur lors de l'envoi du message.")
            self.__s.close()
        
        except OSError:
            print('Serveur introuvable, connexion impossible.')
    
    def _client (self):
        self._send ("clientlist")
        
    def _receive(self, client):
        chunks = []
        finished = False
        while not finished:
            data = client.recv(1024)
            chunks.append(data)
            finished = data == b''
        return b''.join(chunks)