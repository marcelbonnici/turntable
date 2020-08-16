"""
For phase shifts; best of mathfringe & fringeproja
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



def open_csv():
    results = []
    with open("lcherrypick.csv") as csvfile:
        reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC) # change contents to floats
        for row in reader: # each row is a list
            results.append(row)
    return np.asarray(results)

def lookup(table, desired_captured_intensity):#try dci for odd range, evenrange, and none
    table=table[:(np.where(table[:,1]==np.amax(table[:,1]))[0][0])] #makes end of table where first of max capture is
    desired_captured_intensity=int(desired_captured_intensity)
    if desired_captured_intensity<=np.amax(table[:,1]):
        x = np.where(table[:,1] == desired_captured_intensity)
        y = np.where(table[:,1] == 999)

        if len(x[0])==0:
            pdci=desired_captured_intensity
            ndci=desired_captured_intensity
            while len(x[0])==0 and len(y[0])==0:
                pdci=pdci+1
                ndci=ndci-1
                x = np.where(table[:,1] == ndci)
                y = np.where(table[:,1] == pdci)

            if len(x[0])<=len(y[0]):
                x=y

        captured_loc=x[0][int(len(x[0])/2)]
        #if captured_loc>163:
            #print('help')
        projected_loc=table[captured_loc][0]

    else:
        projected_loc=table[-1][0]

    return int(projected_loc)


table=open_csv() #NEW
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

choice=input('Period Quantity(0) or Coefficients(1): ')
n_steps=int(input('Number of Steps: '))

if choice!='1':
    nu0=input('Enter number of periods along x-axis: ')
    try:
        nu0=float(nu0)
    except ValueError:
        nu0=0.25
    xi0=float(input('Enter number of periods along y-axis: '))
    if nu0>0:
        nu0=2*np.pi/(1/nu0)
    if xi0>0:
        xi0=2*np.pi/(1/xi0)
else:
    nu0=float(input('Enter X coefficient: '))
    xi0=float(input('Enter Y coefficient: '))
color=int(input('Grayscale(0) or Default(1): '))
#MOVE
if color==1:
    cmap='viridis'
if color==0:
    cmap='gray'
    color=255
x=np.linspace(0,1,width)
y=np.linspace(0,1,height)
X,Y=np.meshgrid(x,y)

picname=0
I=[]


#LINUX
for cam_number in range(10):
    camera='/dev/video'+str(cam_number)
    subprocess.call(['v4l2-ctl','-d',camera,'--set-ctrl=exposure_auto=1'])

loca=0
for shift in range(n_steps):
    #shift=shift*np.pi/2
    shift=shift*2*np.pi/n_steps
    if cmap=='gray':
        #img=(np.cos(nu0*X+xi0*Y-shift-0*np.pi/2)/2+0.5)*color
        img=(np.cos(nu0*X+xi0*Y-shift-0*np.pi/2)/2+0.5)*190+50
        img=img/255
        img[-1][-1]=0 #image wants to push minimum value (50/255) to total darkness, so I made this negligible pixel zero to prevent compromising other pixels
        img[-2][-1]=1 #instead of pushing maximum value (240/255) to 1, I made a negligible pixel 1 to represent 255/255
        loca=loca+1
        plt.imsave('lphasefringe/'+str(loca)+'.png',img, cmap=cmap)
        if shift == 0:
            plt.imsave('sinusoid.png',img, cmap=cmap)
        I.append(img)
    else:
        img=np.cos(nu0*X+xi0*Y+shift)
        loca=loca+1
        plt.imsave('fringe.png',img, cmap=cmap)
        I.append(img)

    img = mpimg.imread('lphasefringe/'+str(loca)+'.png')
    for j in range (img.shape[1]):
        desired_captured_intensity=img[0,j,0]#i,j,0
        projected_loc=lookup(table, np.around(255*desired_captured_intensity))
        img[:,j]=np.asarray([projected_loc/255,projected_loc/255,projected_loc/255,1])
        #print(i)
    img[-1][-1]=0
    img[-2][-1]=0
    plt.imsave('lphasefringe/'+str(loca)+'.png',img,cmap='gray')



    image = mpimg.imread('lphasefringe/'+str(loca)+'.png')
    #image = mpimg.imread('fringe.png')

    matplotlib.rcParams['toolbar'] = 'None'
    imgplot=plt.imshow(image)
    plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0,
                hspace = 0, wspace = 0)
    manager = plt.get_current_fig_manager() #TkAgg backend
    manager.resize(*manager.window.maxsize()) #TkAgg backend
    manager.full_screen_toggle()
    manager.window.wm_geometry("+500+0")
    plt.show(block=False)

    key=cv2.waitKey(1000)
    picname=picname+1
    cap = cv2.VideoCapture(2) #TO DO: make process automatically find right webcam
    #2 or /dev/v4l/by-id/usb-Sonix_Technology_Co.__Ltd._USB_2.0_Camera_SN0179-video-index0
    cap.set(3,1280)
    cap.set(4,720)
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
    cap.set(cv2.CAP_PROP_EXPOSURE, 40) #800
    i=0
    while(i<3):
        ret, frame = cap.read() #MOD
        if i==2:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imwrite('steppics/'+str(picname)+'.png',gray)
            #cv2.imwrite('wah.png',gray)
        i=i+1
    cap.release()
    key=cv2.waitKey(2)

    plt.close()

    if key == 27:#if ESC is pressed, exit loop
        cv2.destroyAllWindows()
        break
