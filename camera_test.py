"""
For testing if exposure, webcam port, and camera alignment are ideal.
"""
import numpy as np
import cv2
import time
import subprocess
import matplotlib
matplotlib.use('tkagg')
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D

#LINUX
def enable_manual_exposure(port_number):
    '''
    Uses video4linux to enale this parameter for Linux users automatically
    '''
    for cam_number in range(10):
        camera='/dev/video'+str(port_number)
        subprocess.call(['v4l2-ctl','-d',camera,'--set-ctrl=exposure_auto=1'])

def set_camera_params(port_number, width, height):
    '''
    Compares what user tries setting camera resolution to versus what it is
    actually streaming. Helpful for trial-and-error to understand camera's
    possibilities.
    '''
    cap = cv2.VideoCapture(port_number)
    cap.set(3,width)
    cap.set(4,height)
    ret, pic = cap.read()
    print('Webcam\'s Size: '+str(pic.shape[0])+' tall x '+str(pic.shape[1])+' wide')
    return cap

def projector_res():
    '''
    Detect's monitor's resolution to project images to proejctor in full screen
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
    return width, height

def project_white_screen(width, height):
    '''
    Projects full screen pattern once monitor's width and height are found
    '''
    image=127*np.ones((int(height), int(width),3))
    image[int(int(height)/2)-10:int(int(height)/2)+10,int(int(width)/2)-10:int(int(width)/2)+10]=0

    #image = mpimg.imread(fringe_dir+'/'+str(loca)+'.png')
    matplotlib.rcParams['toolbar'] = 'None'
    imgplot=plt.imshow(image)
    plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0,
                hspace = 0, wspace = 0)
    manager = plt.get_current_fig_manager() #TkAgg backend
    manager.resize(*manager.window.maxsize()) #TkAgg backend
    manager.full_screen_toggle()
    manager.window.wm_geometry("+500+0")
    plt.show(block=False)

def exposure_compare(cap, w, h, a, b, c, d, e, f):
    '''
    Compare's two different exposures, and allows user to see intensity at last
    picture. Helpful for choosing a good exposure level for later calibration.
    '''
    speed=0
    while(True):
        if speed<1:
            time_now=time.time()
            cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
            cap.set(cv2.CAP_PROP_EXPOSURE, a)
            ret, gray = cap.read()
            image = cv2.putText(gray, 'Exposure 1', (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2, cv2.LINE_AA)
            speed=speed+(time.time()-time_now)

        elif speed>1 and speed<2:
            time_now=time.time()
            cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
            cap.set(cv2.CAP_PROP_EXPOSURE, b)
            ret, gray = cap.read()
            image = cv2.putText(gray, 'Exposure 2', (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2, cv2.LINE_AA)
            speed=speed+(time.time()-time_now)
        else:
            speed=0

        gray = cv2.rectangle(gray, (int(w/2)-10,int(h/2)-10), (int(w/2)+10,int(h/2)+10), (0,0,255), 2)

        cv2.imshow('frame',gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            avg_color_per_row = np.average(gray[c:d,e:f], axis=0)
            avg_color = np.average(avg_color_per_row, axis=0)
            print('Average pixel intensity (out of 255): '+str(avg_color[1]))
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":

    #Put webcam width and height (px) here
    webcam_width=960
    webcam_height=640

    #Put webcam port number here
    port_number=0

    # Set these two compare exposures, aiming for one below your webcam's noise ceiling. Can be ignored if you are content with your exposure.
    exposure1=50
    exposure2=75

    #Set the cropped area for pixel intensity sample
    top_height_px=100
    bottom_height_px=200
    left_width_px=300
    right_width_px=400


    enable_manual_exposure(port_number)
    cap = set_camera_params(port_number, webcam_width, webcam_height)
    width,height = projector_res()
    project_white_screen(width, height) #also projects dot at middle to help you align camera
    exposure_compare(cap, webcam_width, webcam_height, exposure1, exposure2, top_height_px, bottom_height_px, left_width_px, right_width_px)
