import picamera
import os
import time
import threading

def runAsync(fn):
    def run(*k, **kw):
        t = threading.Thread(target=fn, args=k, kwargs=kw)
        t.start()
        return t
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

        self.ISO = 200
        self.camera.exposure_mode = 'sports'

        self.FPS = None
        self.tpsRendu = None
        self.tpsFonctionnement = None

    @runAsync
    def capturePhoto(self):
        self.TIMESTAMP = time.strftime("%d-%m-%Y_%H-%M-%S")
        self.camera.capture('photo_{}.jpg'.format(self.TIMESTAMP))

    def startTimeLapse(self, FPS, tpsRendu, tpsFonctionnement):
        self.FPS = FPS
        self.tpsRendu = tpsRendu
        self.tpsFonctionnement = tpsFonctionnement
        self.interval = (tpsFonctionnement*3600) / (FPS* tpsRendu)

        print(self.FPS * self.tpsRendu)
        for i in range(0, self.FPS * self.tpsRendu - 1):
            self.capturePhoto()
            time.sleep(self.interval)

    def setSharpness(self, sharpness):
        self.camera.sharpness = sharpness
    def setISO(self, ISO):
        self.camera.iso = ISO
