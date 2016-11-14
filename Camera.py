import subprocess
import threading

class Camera(object):
    def __init__(self, debug=False):
        self.debug = debug

    def checkCamera(self):
        stdout, stderr = self.gphoto2CMD("--auto-dectect")
        return stdout.find("Camera")

    def captureImage(self, path=""):
        self.gphoto2CMD("--capture-image-and-download", "--filename '%Y-%m-%d%_H%:M%:S.jpg'".format(path))
    def captureImageDesync(self, path=""):
        threading._start_new_thread(self.captureImage, (path,))

    def setConfig(self, name, value):
        self.gphoto2CMD("--set-config-value {}={}".format(name, value))

    def gphoto2CMD(self, *cmd):
        #Parse les arguments
        param = ["gphoto2"]
        for arg in cmd:
            arg = arg.split(' ')
            i = 0
            while i < len(arg):
                param.append(arg[i])
                i += 1
                
        if self.debug:
            print(param)

        p = subprocess.Popen(param, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return p.communicate() #Execute la commande et renvoie la sortie

def desyncFunction(function, *kwargs):
    threading._start_new_thread(function, kwargs)
