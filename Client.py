from Networking import Client

client = Client()
client.connect('10.42.42.25', 12345).send({'Ordre':'Timelapse', 'Action':["/home/pi/photo3", 24, 30, 0.25, False]})
reponse = client.recv()
client.close()


