from Networking import Server
import TimeLapse
import Movie


server = Server('', 12345)
server.accept()

while True:
    data = server.recv()
    print(data)

    if data['Ordre'] == 'Timelapse':
        timelapse = TimeLapse.TimeLapse(data["Action"][0])
        timelapse.startTimeLapse(data["Action"][1], data["Action"][2], data["Action"][3], data["Action"][4])

        movie = Movie.MovieHandler(data["Action"][0])
        movie.makeVideo()

        server.send({'Ordre':'Etat_Timelapse', 'Action':True})

server.close()
