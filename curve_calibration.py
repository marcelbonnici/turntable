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
from PIL import Image
import os, os.path
import shutil

class VideoStreamWidget(object): #SOURCE: https://stackoverflow.com/questions/54933801/how-to-increase-performance-of-opencv-cv2-videocapture0-read
    '''
    Calibrates pixel intensities from 1 to 255 for lookup table
    '''
    def __init__(self, src=0):
        self.cap = cv2.VideoCapture(src)

        self.cap.set(3,1280)
        self.cap.set(4,720)
        self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
        self.cap.set(cv2.CAP_PROP_EXPOSURE, 40)
        self.directory='calibration_pics/'

        # Start the thread to read frames from the video stream
        self.thread = Thread(target=self.photograph, args=())
        self.thread.daemon = True
        self.thread.start()

    def open_csv(self):
        '''
        Opens a CSV file to start writing to it
        '''
        results = []
        with open("projection_lookup_table.csv") as csvfile:
            reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
            for row in reader:
                results.append(row)
        return np.asarray(results)

    def width_height(self):
        '''
        Finds monitor width and height to project fullscreen images
        '''
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

        return width,height,self.directory

    def gradient_calibration(self, z):
        '''
        Shifts gradient for certain intensity to be in middle of projection
        '''
        width, height, _=self.width_height()

        img = Image.open('resize_image.png')
        hpercent = (height / float(img.size[1]))
        wsize = int((float(img.size[0]) * float(hpercent)))
        img = img.resize((wsize, height), Image.ANTIALIAS)
        img.save('resize_image.png')

        image=cv2.imread('resize_image.png') #('fringepc.png')
        fail=0
        word='bad'
        middle_index='(array([], dtype=int64), array([], dtype=int64))'
        while str(middle_index)=='(array([], dtype=int64), array([], dtype=int64))':
            middle_index=np.where(image[0][int(width/2):]==z-fail)
            fail=fail+1
        image=image[:,middle_index[0][0]:middle_index[0][0]+int(width)]
        return image

    def image_generate(self, z):
            '''
            Turns calibrated image into uint8 file
            '''
            calibpic=np.full((height,width,3),z)
            calibpic=np.asarray(calibpic,dtype='uint8')

            #calibpic = gradient_calibration(z)

            return calibpic

    def project(self, count, total, image):
        '''
        Puts gradient pattern on projector
        '''
        cv2.namedWindow("fringe", cv2.WND_PROP_FULLSCREEN)
        cv2.moveWindow("fringe",width,0)
        cv2.setWindowProperty("fringe",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        cv2.imshow("fringe", image)

    def each_capture(self, width, height):
        '''
        Carries out entire calibration process
        '''
        captures=255
        for z in range(0,captures+1):
            image=self.gradient_calibration(z)
            self.project(z, captures, image)
            self.photograph(z, self.cap)
            key=cv2.waitKey(2)
            if key == 27:#if ESC is pressed, exit loop
                cap.release()
                cv2.destroyAllWindows()
                break

    def photograph(self, z, cap):
        '''
        Camera takes 5 pictures at each calibration projection, to minimize
        artifacts' influence
        '''
        # Read the next frame from the stream in a different thread
        key=cv2.waitKey(2)
        i=0
        print(z)
        while(i<=6):
            self.status, self.frame = cap.read()
            if i>1:
                gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
                cv2.imwrite(self.directory+str(z)+'-'+str(i-2)+'.png',gray[200:-200,:])#Index CHANGED
            i=i+1

        key = cv2.waitKey(1)
        if key == ord('q'):
            self.cap.release()
            cv2.destroyAllWindows()
            exit(1)

    def sample_image_intensities(self):
        '''
        Determines captured intensity to compare to ideal, projected intensity
        '''
        sample=np.array([])
        for i in range(1, 256):
            intensity_avg=np.array([])
            for j in range(5):
                pic=cv2.imread(self.directory+str(i)+'-'+str(j)+'.png')
                pic=np.mean(pic[:,int(pic.shape[1]/2)])
                intensity_avg=np.append(intensity_avg, pic)
            intensity_avg=np.mean(intensity_avg)
            sample=np.append(sample,intensity_avg)
        return sample

    def generate_polyfit_calibration_curve(self):
        '''
        Compares a projected gradient image to the capture of the projection on a white wall, making a lookup csv with the best results
        '''

        width, height, _ = self.width_height()

        plt.rcParams.update({'font.size': 22})
        basis=cv2.imread('basis.png')[int(height/2),int(width/2):]

        sample = self.sample_image_intensities()

        cherries=np.array([])
        slength=int(sample.shape[0])
        blength=int(basis.shape[0])

        x=np.arange(1,256)
        y=sample
        z=np.polyfit(x,y,11)
        p=np.poly1d(z)
        xp=np.linspace(x,y, num=255)
        p=p(xp)
        yp=p
        rows = np.asarray(np.array([xp,yp]).T,dtype='int')[:,0]
        rows=rows[int(np.where(rows[:,0]==1)[0][0]):]
        np.savetxt('projection_lookup_table.csv', rows, delimiter=",", fmt='%d')
        fig, ax = plt.subplots()
        ax.plot(x, y, '-b', label='Before Line Fitting')
        ax.plot(xp, yp, '-r', label='After Line Fitting')
        leg = ax.legend()

        plt.xlabel('Projected Intensity', fontsize=18)
        plt.ylabel('Captured Intensity', fontsize=18)
        plt.title('Radiometric Calibration Curve for Input Image', fontsize=18)
        plt.show()

if __name__ == "__main__":
    #SEE __INIT__ FOR VALUES, LIKE WIDTH, HEIGHT AND EXPOSURE, TO CHANGE TO YOUR LIKING
    video_stream_widget = VideoStreamWidget()
    width, height, directory = video_stream_widget.width_height() # Find width and height of monitor for projection

    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)

    video_stream_widget.each_capture(width, height) # Photographs and projects. The meat of this script
    video_stream_widget.generate_polyfit_calibration_curve() # Look to validate the data looks like it follows a smooth curve
