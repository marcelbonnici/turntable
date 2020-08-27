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
import t.urn as turn


def open_csv(directory):
    results = []
    with open(directory) as csvfile:
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


#Alternative method for pixel-by-pixel calibration; yielded subpar fringes before project deadline
def lookup_pixel(table, desired_captured_intensity, height):
    table=table[:(np.where(table[:,height+1]==np.amax(table[:,height+1]))[0][0])] #makes end of table where first of max capture is
    desired_captured_intensity=int(desired_captured_intensity)

    if desired_captured_intensity<=np.amax(table[:,height+1]):
        x = np.where(table[:,height+1] == desired_captured_intensity)
        y = np.where(table[:,height+1] == 999)

        if len(x[0])==0:
            pdci=desired_captured_intensity
            ndci=desired_captured_intensity
            while len(x[0])==0 and len(y[0])==0:
                pdci=pdci+1
                ndci=ndci-1
                x = np.where(table[:,height+1] == ndci)
                y = np.where(table[:,height+1] == pdci)

            if len(x[0])<=len(y[0]):
                x=y

        captured_loc=x[0][int(len(x[0])/2)]
        projected_loc=table[captured_loc][0]

    else:
        projected_loc=table[-1][0]

    return int(projected_loc)

def screen_res():
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

def user_input():
    n_steps=int(input('Number of Steps: '))
    frac = int(input('Number of fractions of Rotations: '))
    nu0=input('Enter a LOW number of periods along x-axis: ')
    try:
        nu0=float(nu0)
    except ValueError:
        nu0=0.25
    xi0=float(input('Enter a LOW number of periods along y-axis: '))
    if nu0>0:
        nu0=2*np.pi/(1/nu0)
    if xi0>0:
        xi0=2*np.pi/(1/xi0)

    nu1=input('Enter a HIGH number of periods along x-axis: ')
    try:
        nu1=float(nu1)
    except ValueError:
        nu1=0.25
    xi1=float(input('Enter a HIGH number of periods along y-axis: '))
    if nu1>0:
        nu1=2*np.pi/(1/nu1)
    if xi1>0:
        xi1=2*np.pi/(1/xi1)

    return n_steps, frac, nu0, xi0, nu1, xi1

def fringe_create(shift, n_steps, nu0, X, xi0, Y, loca, fringe_dir):
    shift=shift*2*np.pi/n_steps
    img=(np.cos(nu0*X+xi0*Y-shift-0*np.pi/2)/2+0.5)*190+50 #eliminates noise floor and ceiling in cameras
    img=img/255
    img[-1][-1]=0 #image wants to push minimum value (50/255) to total darkness, so I made this negligible pixel zero to prevent compromising other pixels
    img[-2][-1]=1 #instead of pushing maximum value (240/255) to 1, I made a negligible pixel 1 to represent 255/255
    loca=loca+1
    plt.imsave(fringe_dir+'/'+str(loca)+'.png',img, cmap='gray')
    return loca

def fringe_convert(table, loca, fringe_dir):
    img = mpimg.imread(fringe_dir+'/'+str(loca)+'.png')
    for j in range (img.shape[1]):
        desired_captured_intensity=img[0,j,0]
        projected_loc=lookup(table, np.around(255*desired_captured_intensity))
        img[:,j]=np.asarray([projected_loc/255,projected_loc/255,projected_loc/255,1])
    img[-1][-1]=0
    img[-2][-1]=0
    plt.imsave(fringe_dir+'/'+str(loca)+'.png',img,cmap='gray')

def project (fringe_dir, loca):
    image = mpimg.imread(fringe_dir+'/'+str(loca)+'.png')
    matplotlib.rcParams['toolbar'] = 'None'
    imgplot=plt.imshow(image)
    plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0,
                hspace = 0, wspace = 0)
    manager = plt.get_current_fig_manager() #TkAgg backend
    manager.resize(*manager.window.maxsize()) #TkAgg backend
    manager.full_screen_toggle()
    manager.window.wm_geometry("+500+0")
    plt.show(block=False)

def camera_setup(picname, exposur, cam_width, cam_height, portno):
    key=cv2.waitKey(1000)
    picname=picname+1
    cap = cv2.VideoCapture(portno)
    cap.set(3,int(cam_width))
    cap.set(4,int(cam_height))
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
    cap.set(cv2.CAP_PROP_EXPOSURE, exposur) #800
    time.sleep(1)
    return cap

def photoshoot(cap, pic_dir, picname):
    i=0
    while(i<=6):
        ret, frame = cap.read()
        if i>1:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(pic_dir+'/'+str(picname)+'-'+str(i-2)+'.png',gray)
        i=i+1

def everything(data_folder, table, width, height, portno, exposur, cam_width, cam_height):

    subprocess.call(['v4l2-ctl','-d',str(portno),'--set-ctrl=exposure_auto=1'])
    picname=0
    x=np.linspace(0,1,width)
    y=np.linspace(0,1,height)
    X,Y=np.meshgrid(x,y)

    n_steps, divisions, nu0, xi0, nu1, xi1 = user_input()

    for i in range(2):
        loca=0
        if i == 1: #Changes between projecting low frequency and high frequency
            nu0=nu1
            xi0=xi1
            pic_dir=data_folder+'/high_pics'
            fringe_dir=data_folder+'/high_fringe'
        else:
            pic_dir=data_folder+'/low_pics'
            fringe_dir=data_folder+'/low_fringe'

        for j in range (divisions):
            if divisions != 1:
                turn.degrees(360/divisions)
                time.sleep(35/int(np.abs(divisions)))

            for shift in range(n_steps):
                loca = fringe_create(shift, n_steps, nu0, X, xi0, Y, loca, fringe_dir)
                fringe_convert(table, loca, fringe_dir)
                project(fringe_dir, loca)
                cap = camera_setup(picname, exposur, cam_width, cam_height, portno)
                photoshoot(cap, pic_dir, picname)

                # Close everything
                cap.release()
                key=cv2.waitKey(2)
                plt.close()
                if key == 27:#if ESC is pressed, exit loop
                    cv2.destroyAllWindows()
                    break

if __name__ == "__main__":
    table=open_csv("lcherrypick.csv")

    data_folder='turn_pics'

    portno=0
    exposur=40
    cam_width=1280
    cam_height=720

    width, height = screen_res()
    everything(data_folder, table, width, height, portno, exposur, cam_width, cam_height)
