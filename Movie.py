import subprocess

class MovieHandler(object):
    def __init__(self, path, FPS):
        if(path[-1] == '/'):
            self.path = path
        else:
            self.path = path + '/'
        self.FPS = path

    def resizeImage(self):
        pass

    def makeVideo(self):
        p = subprocess.Popen('mencoder {}*.jpg on:fps={}:type=jpeg -ovc lavc -lavcopts vcodec=mjpeg -o timelapse.avi'.format(self.path, self.FPS), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return p.communicate()
