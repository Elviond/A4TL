# coding: utf8

import logging
import os
import threading
import time

import picamera

"""
	Lance la fonction passée en paramètre dans un nouveau thread
"""

def runAsync(fn):
    def run(*k, **kw):
        t = threading.Thread(target=fn, args=k, kwargs=kw)
        t.start()
        return t

    return run


"""
	Mesure le temps écoulé
"""

class Timer(object):
    def __init__(self):
        pass
    def startTimer(self):
        self.oldTime = time.time()

    def stopTimer(self):
        self.newTime = time.time()

    def getTime(self, precision=6):
        """
            Retourne le temps avec x chiffres après la virgule
        """
        return round(self.newTime - self.oldTime, precision)


class TimeLapse(object):
    def __init__(self, path):
        # Formatage du chemin du dossier de travail
        if path[-1] == '/':
            self.path = path
        else:
            self.path = path + '/'
        # On se place dans le dossier de travail
        os.chdir(path)

        # Camera Raspberry
        # TODO: Externaliser tout ça
        self.camera = picamera.PiCamera()
        self.camera.resolution = (1920, 1080)
        self.camera.exposure_mode = 'auto'

        # Utils
        self.timer = Timer()

        # Logger
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

        self.steam_handler = logging.StreamHandler()
        self.steam_handler.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
        self.logger.addHandler(self.steam_handler)

        self.FPS = None
        self.tpsRendu = None
        self.tpsFonctionnement = None
        self.currentImg = None

    def capturePhoto(self, number):
        # self.TIMESTAMP = time.strftime("%d-%m-%Y_%H-%M-%S")
        # self.camera.capture('photo_{}.jpg'.format(self.TIMESTAMP))
        self.camera.capture('photo_{}.jpg'.format(number))

    def startTimeLapse(self, FPS, tpsRendu, tpsFonctionnement, isAsync=False):
        self.FPS = FPS
        self.tpsRendu = tpsRendu
        self.tpsFonctionnement = tpsFonctionnement
        self.interval = (tpsFonctionnement * 3600) / (FPS * tpsRendu)

        for i in range(0, self.FPS * self.tpsRendu):
            self.logger.debug("{} / {}".format(i + 1, self.FPS * self.tpsRendu))

            # TODO: Check si interval < 8s

            if isAsync:
                threading._start_new_thread(target=self.capturePhoto, args=i)
            else:
                self.timer.startTimer()
                self.capturePhoto(i)
                self.timer.stopTimer()

            self.delay = self.interval - self.timer.getTime()
            if self.delay <= 0:
                continue
            else:
                time.sleep(self.delay)

            self.currentImg = i

    def setSharpness(self, sharpness):
        self.camera.sharpness = sharpness

    def setISO(self, ISO):
        self.camera.iso = ISO

    def sendVideo(self):
        p = os.popen('nc -l -p 12345 < TimeLapse.mp4')


"""
path = "/home/pi/photo2"

timelapse = TimeLapse(path)
timelapse.startTimeLapse(24, 30, 0.25, False)
movie = Movie.MovieHandler(path, 24)
movie.makeVideo()
timelapse.sendVideo()
"""
