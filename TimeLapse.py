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
    def __init__(self, path, FPS=24, tpsRendu, tpsFonctionnement):
        if (path[-1] == '/'):
            self.path = path
        else:
            self.path = path + '/'
        # On se place dans le dossier de travail
        os.chdir(path)


        #Configuration de la Camera Raspberry (va être déplacé dans une classe à part)
        self.camera = picamera.PiCamera()
        self.ISO = 200
        self.camera.exposure_mode = 'sports'

        self.FPS = FPS
        self.tpsRendu = tpsRendu
        self.tpsFonctionnement = tpsFonctionnement

    @runAsync
    def capturePhoto(self):
        self.TIMESTAMP = time.strftime("%d-%m-%Y_%H-%M-%S")
        self.camera.capture('photo_{}.jpg'.format(self.TIMESTAMP))

    def startTimeLapse(self):
        self.interval = (self.tpsFonctionnement*3600) / (self.FPS* self.tpsRendu)

        print(self.FPS * self.tpsRendu)
        for i in range(0, self.FPS * self.tpsRendu - 1):
            self.capturePhoto()
            time.sleep(self.interval)

    def setSharpness(self, sharpness):
        self.camera.sharpness = sharpness
    def setISO(self, ISO):
        self.camera.iso = ISO
