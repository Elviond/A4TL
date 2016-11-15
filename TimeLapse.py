import picamera
import os
import time
import threading

def runAsync(fn):
    def run(*k, **kw):
        t = threading.Thread(target=fn, args=k, kwargs=kw)
        t.start()
    return run

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

        self.FPS = None
        self.tpsRendu = None
        self.tpsFonctionnement = None

    @runAsync
    def capturePhotoSync(self):
        self.TIMESTAMP = time.strftime("%d-%m-%Y_%H:%M:%S")
        self.camera.capture('photo_{}.jpg'.format(self.TIMESTAMP))

    def startTimeLapse(self, FPS, tpsRendu, tpsFonctionnement):
        self.interval = (FPS* tpsRendu) / (tpsFonctionnement*3600)

    @runAsync
    def test(self):
        for i in range(10):
            print('yolo')

