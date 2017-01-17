# -*- coding: UTF-8 -*-


import select
import socket
import TimeLapse
import Movie

timelapse = None
movie = None
timeLapseState = False

class Server(object):

    # @param port Port de connexion
    # @param listen Nombre de connexion en attente max
    def __init__(self, port=35890, listen=1):

        self.nbClients = 0  # Nombre de client connecté
        self.sockets = []  # Liste des sockets client

        # Création du socket serveur
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # On passe le socket serveur en non-bloquant
        self.socket.setblocking(0)
        # On attache le socket au port d'écoute.
        self.socket.bind(('', port))

        self.socket.listen(listen)

    # @param socket Socket sur lequelle il faut recuperer les données
    # @return Données envoyées par le client
    def receive(self, socket):
        buf = ""  # Variable dans laquelle on stocke les données
        _hasData = True  # Nous permet de savoir si il y de données à lire
        while _hasData:
            # On passe le socket en non-bloquant
            socket.setblocking(0)
            try:
                _data = socket.recv(256)
                if (_data):
                    buf += _data
                else:
                    # Déconnexion du client
                    _hasData = False
            except:
                _hasData = False
        return buf

    # Fonction qui lance les sockets et s'occupe des clients
    def run(self):
        # On ajoute le socket serveur à la liste des sockets
        self.sockets.append(self.socket)
        while True:
            try:
                readReady, writeReady, nothing = select.select(self.sockets, self.sockets, [])
            except select.error as e:
                break
            except socket.error as e:
                break

            # On parcours les sockets qui ont reçus des données
            for sock in readReady:
                if sock == self.socket:
                    # C'est le socket serveur qui a reçus des données
                    # Cela signifie qu'un client vient de se connecter
                    # On accept donc ce client et on récupère qques infos
                    client, address = self.socket.accept()
                    self.nbClients += 1
                    # On ajoute le socket client dans la liste des sockets
                    self.sockets.append(client)
                else:
                    # Le client a envoyé des données, on essaye de les lire
                    try:
                        data = self.receive(sock)
                        if data:
                            # On renvoi au client ce qu'il a envoyé
                            sock.send(data)
                            self.processData(data, sock)
                        else:
                            self.nbClients -= 1
                            self.sockets.remove(sock)
                    except socket.error as e:
                        self.sockets.remove(sock)

    def sendSerialized(self, data, sock):
        sock.send(str(data))

    def processData(self, data, sock):
        self.data = eval(data)

        self.ordre = self.data['Action']
        self.params = self.data["Params"]

        if self.ordre == 'Timelapse':
            global timelapse
            timelapse = TimeLapse.TimeLapse(self.params[0])
            timelapse.startTimeLapse(self.params[1], self.params[2], self.params[3], self.params[4])

            global movie
            movie = Movie.MovieHandler(self.params[0], self.params[1])
            movie.makeVideo()

            global timeLapseState
            timeLapseState = True

        if self.ordre == 'getState':
            self.sendSerialized({'Action': 'TimelapseState', 'Params': timeLapseState}, sock)

        if self.ordre == 'sendVideo':
            timelapse.sendVideo()


server = Server(42420, 1)
server.run()
