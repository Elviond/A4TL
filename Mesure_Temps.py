import picamera
import time

camera = picamera.PiCamera()
camera.exposure_mode = 'auto'

def writeMesures(temps_pose, temps, i):
    with open("temps_pose.csv", 'a') as temps_pose_file:
        temps_pose_file.write(str(temps_pose).replace('.', ',') + '\n')
    with open("temps.csv", 'a') as temps_file:
        temps_file.write(str(temps).replace('.', ',') + '\n')

    print(str(temps) + ' ' + str(temps_pose) + ' {} / {}'.format(i+1, etendue))
    
etendue = 1440
start_time = time.time()
for i in range(0, etendue):
    t0 = time.time()
    camera.capture("mesure.jpg")
    temps_pose = time.time() - t0
    writeMesures(temps_pose, time.time() - start_time, i)

