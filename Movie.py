import subprocess
import os

class MovieHandler(object):
    def __init__(self, path, FPS):
        self.path = path
        os.chdir(path)

    def resizeImage(self, lenght, width):
        p = subprocess.Popen('convert *.jpg -geometry'.format(self.FPS), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return p.communicate()

    def makeVideo(self):
        p = subprocess.Popen('avconv -r {FPS} -i photo_%d.jpg video.mp4'.format(self.FPS), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return p.communicate()
