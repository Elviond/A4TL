import picamera
import os
import time
import threading
import subprocess
import Movie

def runAsync(fn):
    def run(*k, **kw):
        t = threading.Thread(target=fn, args=k, kwargs=kw)
        t.start()
        return t
    return run

class Timer(object):
    def __init__(self):
        self.oldTime = -1

    def startTimer(self):
        self.oldTime = round(time.time(), 3)
    def stopTimer(self):
        self.newTime = round(time.time(), 3)
    def getDifference(self):
        return self.newTime - self.oldTime

class TimeLapse(object):
    def __init__(self, path):
        if (path[-1] == '/'):
            self.path = path
        else:
            self.path = path + '/'
        # On se place dans le dossier de travail
        os.chdir(path)


        #Camera Raspberry
        self.camera = picamera.PiCamera()
        self.camera.resolution = (1920, 1080)

        self.ISO = 300
        self.camera.exposure_mode = 'sports'

        self.FPS = None
        self.tpsRendu = None
        self.tpsFonctionnement = None

    #@runAsync
    def capturePhoto(self,number):
        #self.TIMESTAMP = time.strftime("%d-%m-%Y_%H-%M-%S")
        #self.camera.capture('photo_{}.jpg'.format(self.TIMESTAMP))
        self.camera.capture('photo_{}.jpg'.format(number))

    def startTimeLapse(self, FPS, tpsRendu, tpsFonctionnement, isAsync=True):
        self.FPS = FPS
        self.tpsRendu = tpsRendu
        self.tpsFonctionnement = tpsFonctionnement
        self.interval = (tpsFonctionnement*3600) / (FPS* tpsRendu)

        for i in range(0, self.FPS * self.tpsRendu):
            print("{} / {}".format(i+1, self.FPS * self.tpsRendu))

            #TODO: Check si interval < 8s

            if isAsync:
                threading._start_new_thread(target=self.capturePhoto, args=i)
            else:
                self.oldTime = int(round(time.time()) * 1000)
                self.capturePhoto(i)
                self.delay = self.interval - (int(round(time.time() * 1000)) - self.oldTime) * 0.001

                if self.delay <= 0:
                    continue
                else:
                    time.sleep(self.delay)


    def setSharpness(self, sharpness):
        self.camera.sharpness = sharpness
    def setISO(self, ISO):
        self.camera.iso = ISO
    def makeVideo(self):
        pass
    def sendVideo(self):
        #logging.info("Serveur video demare")
        p = subprocess.Popen('nc -l -p 12345 < TimeLapse.mp4', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return p.communicate()

path = "/home/pi/photo2"

timelapse = TimeLapse(path)
timelapse.startTimeLapse(24, 30, 0.25, False)
movie = Movie.MovieHandler(path)
movie.makeVideo()
timelapse.sendVideo()
