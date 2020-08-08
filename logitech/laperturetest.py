"""
For testing if camera, exposure, and so on is working ni real-time. For quick & messy testing
"""
import numpy as np
import cv2
import time
import subprocess
#Enable manual exposure in terminal:   v4l2-ctl -d /dev/video2 --set-ctrl=exposure_auto=1

#LINUX
for cam_number in range(10):
    camera='/dev/video'+str(cam_number)
    subprocess.call(['v4l2-ctl','-d',camera,'--set-ctrl=exposure_auto=1'])

cap = cv2.VideoCapture(4)
#2 or /dev/v4l/by-id/usb-Sonix_Technology_Co.__Ltd._USB_2.0_Camera_SN0179-video-index0
w=1280
h=720
cap.set(3,w)
cap.set(4,h)
speed=0
exposure=83
while(True):
    # Capture frame-by-frame
    if speed<1:
        time_now=time.time()
        cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
        cap.set(cv2.CAP_PROP_EXPOSURE, exposure)
        ret, gray = cap.read()
        #image = cv2.putText(gray, '312us', (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2, cv2.LINE_AA)
        speed=speed+(time.time()-time_now)
    elif speed>1 and speed<2:
        time_now=time.time()
        cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
        cap.set(cv2.CAP_PROP_EXPOSURE, exposure)#good 'ol 800
        ret, gray = cap.read()
        #image = cv2.putText(gray, '22ms', (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2, cv2.LINE_AA)
        speed=speed+(time.time()-time_now)
    else:
        speed=0
    # Our operations on the frame come here
    #gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)

    gray = cv2.rectangle(gray, (int(w/2)-10,int(h/2)-10), (int(w/2)+10,int(h/2)+10), (255,0,0), 2)
    # Display the resulting frame
    gray=gray[155:-155,280:-210]
    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        #cv2.imwrite('avgintensity.jpg',gray)
        avg_color_per_row = np.average(gray, axis=0)
        avg_color = np.average(avg_color_per_row, axis=0)
        print(avg_color[0])
        #print(np.average(gray[240]))
        cv2.imwrite('sample.png', gray)
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
