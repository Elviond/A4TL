from Networking import Client
import os

def getVideo(ip, port):
    client.send({'Action': 'sendVideo', 'Params': []})
    p = os.popen("nc -w 3 {} {} > Timelapse.mp4".format(ip, port))

def sendData(data):
    client.send(data)
    getData()

def getData():
    check = client.recv()
    print(check)

client = Client()
client.connect('10.42.42.25', 42420)
sendData({'Action':'Timelapse', 'Params':["/home/pi/photo3", 24, 10, 1/48, False]})
i = input("Video ?")
getVideo('10.42.42.25', 12345)

client.close()
