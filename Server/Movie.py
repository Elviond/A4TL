import subprocess
import os

class MovieHandler(object):
    def __init__(self, path, FPS):
        self.path = path
        self.FPS = FPS
        os.chdir(path)

    def resizeImage(self, lenght, width):
        p = os.popen('convert *.jpg -geometry'.format(self.FPS))

    def makeVideo(self):
        p = os.popen('avconv -r {} -i photo_%d.jpg TimeLapse.mp4'.format(self.FPS))
