from Networking import Server
import TimeLapse
import Movie


server = Server('', 12345)
server.accept()

while True:
    data = server.recv()
    print(data)

    if data['Ordre'] == 'Timelapse':
        timelapse = TimeLapse.TimeLapse(data["Ordre"][0])
        timelapse.startTimeLapse(data["Ordre"][1], data["Ordre"][2], data["Ordre"][3], data["Ordre"][4])

        movie = Movie.MovieHandler(data["Ordre"][0])
        movie.makeVideo()

        server.send({'Ordre':'Etat_Timelapse', 'Action':True})

server.close()
