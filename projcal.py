import numpy as np
import matplotlib.pyplot as plt
import cv2
import time
import screeninfo
import subprocess

screencount=0
for m in screeninfo.get_monitors():
    width = int(m.width)
    height = int(m.height)

for z in range(int(255/10)+2):#255
    if z!=0:
        z=(z*10)-5
    calibpic=np.full((height,width,3),z)

    calibpic=np.asarray(calibpic,dtype='uint8')
    plt.imsave('calib.jpg',calibpic)
    image = cv2.imread('calib.jpg')
    cv2.namedWindow("fringe", cv2.WND_PROP_FULLSCREEN)
    cv2.moveWindow('fringe',int(m.width),0)
    cv2.setWindowProperty("fringe",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

    cv2.imshow('fringe', image)
    print(image[0][0])

    #subprocess.call(["v4l2-ctl", "-d", "/dev/video3", "-c", "exposure_auto=1", "-c", "exposure_absolute=50"])
    key=cv2.waitKey(2)
    cap = cv2.VideoCapture(2) #TO DO: make process automatically find right webcam
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
    cap.set(cv2.CAP_PROP_EXPOSURE, 750)#1000
    i=0
    while(i<3):
        ret, frame = cap.read() #MOD
        if i==2:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imwrite('calib/'+str(z)+'.png',gray)#+str(z)
        i=i+1
    cap.release()
    key=cv2.waitKey(2)

    if key == 27:#if ESC is pressed, exit loop
        cv2.destroyAllWindows()
        break
