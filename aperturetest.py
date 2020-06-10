"""
For testing if camera, exposure, and so on is working ni real-time. For quick & messy testing
"""
"""
import numpy as np
import cv2

cap = cv2.VideoCapture(2)

cap.set(cv2.CAP_PROP_FRAME_WIDTH,3264)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,2448)
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
cap.set(cv2.CAP_PROP_EXPOSURE, 400)
while(True):

    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.imwrite('calib.jpg',gray)
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
"""

import numpy as np
import cv2
import time

cap = cv2.VideoCapture(2)

speed=0
while(True):
    # Capture frame-by-frame


    if speed<1:
        time_now=time.time()
        cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
        cap.set(cv2.CAP_PROP_EXPOSURE, 300)
        ret, gray = cap.read()
        #image = cv2.putText(gray, '312us', (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2, cv2.LINE_AA)
        speed=speed+(time.time()-time_now)
    elif speed>1 and speed<2:
        time_now=time.time()
        cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
        cap.set(cv2.CAP_PROP_EXPOSURE, 220)
        ret, gray = cap.read()
        #image = cv2.putText(gray, '22ms', (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2, cv2.LINE_AA)
        speed=speed+(time.time()-time_now)
    else:
        speed=0
    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.imwrite('pitchblacktest1.png',gray)
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
