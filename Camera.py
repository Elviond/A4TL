import subprocess
import time

class Camera(object):
    def __init__(self):
        pass

    def checkCamera(self):
        stdout, stderr = self.gphoto2CMD("--auto-dectect")
        return stdout.find("Camera")

    def captureImage(self, path=""):
        TIMESTAMP = time.strftime("%Y-%m-%d_%H-%M-%S")
        self.gphoto2CMD("--capture-image-and-download", "--filename {}timelaspe_{}.jpeg".format(path, TIMESTAMP))

    def gphoto2CMD(self, *cmd):
        #Parse les arguments
        param = ["gphoto2"]
        for arg in cmd:
            arg = arg.split(' ')
            i = 0
            while i < len(arg):
                param.append(arg[i])
                i += 1
        print(param)
        p = subprocess.Popen(param, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return p.communicate() #Execute la commande et renvoie la sortie
