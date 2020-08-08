"""
Photographing for calibration
"""
import numpy as np
import matplotlib
matplotlib.use('tkagg')
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2
import time
import subprocess
import csv
from threading import Thread

class VideoStreamWidget(object): #SOURCE: https://stackoverflow.com/questions/54933801/how-to-increase-performance-of-opencv-cv2-videocapture0-read
    def __init__(self, src=4):
        self.cap = cv2.VideoCapture(src)

        self.cap.set(3,1280)#3264 CHANGED
        self.cap.set(4,720)#2448 CHANGED
        self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
        self.cap.set(cv2.CAP_PROP_EXPOSURE, 83) #800 CHANGED
        self.directory='lcalibgradient/'

        # Start the thread to read frames from the video stream
        self.thread = Thread(target=self.photograph, args=())
        self.thread.daemon = True
        self.thread.start()

    def open_csv(self):
        results = []
        with open("fitplot.csv") as csvfile:
            reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC) # change contents to floats
            for row in reader: # each row is a list
                results.append(row)
        return np.asarray(results)

    def width_height(self):
        cmd = ['xrandr']
        cmd2 = ['grep', '*']
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        p2 = subprocess.Popen(cmd2, stdin=p.stdout, stdout=subprocess.PIPE)
        p.stdout.close()
        resolution_string, junk = p2.communicate()
        resolution = resolution_string.split()[0]
        width, height = str(resolution).split('x')
        width=int(width[2:])
        height=int(height[:-1])
        return width,height

    def gradient_calibration(self, z):
        image=cv2.imread('lbasis50240.png')#('fringepc.png')
        fail=0
        word='bad'
        middle_index='(array([], dtype=int64), array([], dtype=int64))'
        while str(middle_index)=='(array([], dtype=int64), array([], dtype=int64))':
            middle_index=np.where(image[0][960:]==z-fail)
            fail=fail+1
        image=image[:,middle_index[0][0]:middle_index[0][0]+1920]
        return image

    def image_generate(self, z):
            calibpic=np.full((height,width,3),z)
            calibpic=np.asarray(calibpic,dtype='uint8')

            #calibpic = gradient_calibration(z)

            return calibpic

    def project(self, count, total, image):
        cv2.namedWindow("fringe", cv2.WND_PROP_FULLSCREEN)
        cv2.moveWindow("fringe",width,0)
        cv2.setWindowProperty("fringe",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        cv2.imshow("fringe", image)
        #print(str(count)+ ' of ' + str(total))

    def each_capture(self, width, height):
        captures=255
        for z in range(50,captures+1):
            #projected_loc=lookup(table, z)
            image=self.gradient_calibration(z)#image_generate(z) CHANGED
            self.project(z, captures, image)
            self.photograph(z, self.cap)
            key=cv2.waitKey(2)
            if key == 27:#if ESC is pressed, exit loop
                cap.release()
                cv2.destroyAllWindows()
                break

    def photograph(self, z, cap):
        # Read the next frame from the stream in a different thread
        key=cv2.waitKey(2)
        i=0
        print(z)
        while(i<=6):#(i<=51):
            self.status, self.frame = cap.read() #MOD
            #(ret,frame) = video_stream_widget.update()
            if i>1:
                gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
                cv2.imwrite(self.directory+str(z)+'-'+str(i-2)+'.png',gray[155:-155,280:-210])#Index CHANGED
            i=i+1

        key = cv2.waitKey(1)
        if key == ord('q'):
            self.cap.release()
            cv2.destroyAllWindows()
            exit(1)

if __name__ == "__main__":
    video_stream_widget = VideoStreamWidget()
    #table = video_stream_widget.open_csv()
    width, height = video_stream_widget.width_height()
    video_stream_widget.each_capture(width, height)
