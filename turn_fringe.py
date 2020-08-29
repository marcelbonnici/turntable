"""
For phase shifts; best of mathfringe & fringeproja
"""
import matplotlib
matplotlib.use('tkagg')
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D

import numpy as np
from PIL import Image
import cv2
import time
import subprocess
import csv
import os, os.path
import shutil
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
    divisions = int(input('Number of fractions of Rotations: '))
    nu00=input('Enter a LOW number of periods along x-axis: ')
    try:
        nu00=float(nu00)
    except ValueError:
        nu00=0.25
    xi00=0 # Was not reached but something like: float(input('Enter a LOW number of periods along y-axis: '))
    if nu00>0:
        nu00=2*np.pi/(1/nu00)
    if xi00>0:
        xi00=2*np.pi/(1/xi00)

    nu1=input('Enter a HIGH number of periods along x-axis: ')
    try:
        nu1=float(nu1)
    except ValueError:
        nu1=0.25
    xi1=0 # Was not reached but something like: float(input('Enter a HIGH number of periods along y-axis: '))
    if nu1>0:
        nu1=2*np.pi/(1/nu1)
    if xi1>0:
        xi1=2*np.pi/(1/xi1)

    return n_steps, divisions, nu00, xi00, nu1, xi1

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
    return cap, picname

def photoshoot(cap, pic_dir, picname):
    k=0
    while(k<=6):
        ret, frame = cap.read()
        if k>1:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(pic_dir+'/'+str(picname)+'-'+str(k-2)+'.png',gray)
        k=k+1

def make_folders(data_folder, divisions):
    for m in range(divisions):
        deg_folder = m * int(360/divisions)
        folder = str(data_folder)+'/'+str(deg_folder)
        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.makedirs(folder)

def toggle_low_high(i, nu00, xi00, nu1, xi1, data_folder, deg_folder):
    if i == 1: #Changes between projecting low frequency and high frequency
        nu0=nu1
        xi0=xi1
        pic_dir=data_folder+'/'+str(deg_folder)+'/high_pics'
        if os.path.exists(pic_dir):
            shutil.rmtree(pic_dir)
        os.makedirs(pic_dir)

        fringe_dir=data_folder+'/'+str(deg_folder)+'/high_fringe'
        if os.path.exists(fringe_dir):
            shutil.rmtree(fringe_dir)
        os.makedirs(fringe_dir)
    else:
        nu0=nu00
        xi0=xi00
        pic_dir=data_folder+'/'+str(deg_folder)+'/low_pics'
        if os.path.exists(pic_dir):
            shutil.rmtree(pic_dir)
        os.makedirs(pic_dir)
        fringe_dir=data_folder+'/'+str(deg_folder)+'/low_fringe'
        if os.path.exists(fringe_dir):
            shutil.rmtree(fringe_dir)
        os.makedirs(fringe_dir)

    return xi0, nu0, pic_dir, fringe_dir

def projection_folders(i, data_folder, j, divisions):
    if i == 1:
        fringe_dir=data_folder+'/'+str(j*int(360/divisions))+'/high_fringe'
        pic_dir=data_folder+'/'+str(j*int(360/divisions))+'/high_pics'
    else:
        fringe_dir=data_folder+'/'+str(j*int(360/divisions))+'/low_fringe'
        pic_dir=data_folder+'/'+str(j*int(360/divisions))+'/low_pics'
    return fringe_dir, pic_dir

def procedure(folder, table, width, height, portno, exposur, cam_width, cam_height):

    subprocess.call(['v4l2-ctl','-d',str(portno),'--set-ctrl=exposure_auto=1'])
    x=np.linspace(0,1,width)
    y=np.linspace(0,1,height)
    X,Y=np.meshgrid(x,y)

    n_steps, divisions, nu00, xi00, nu1, xi1 = user_input()

    for q in range(2):
        if q==0:
            data_folder=folder+'/wall'
            input("Clear off turntable. Press Enter to continue.")
        else:
            data_folder=folder+'/subject'
            input("Place object on turntable. Press Enter to continue.")


        make_folders(data_folder, divisions)

        for i in range(2):
            for p in range (divisions):
                deg_folder = p * int(360/divisions)

                xi0, nu0, pic_dir, fringe_dir = toggle_low_high(i, nu00, xi00, nu1, xi1, data_folder, deg_folder)

            for j in range(1,divisions+1):
                loca=0
                picname=0

                #if divisions > 1:
                turn.degrees(360/divisions)
                time.sleep(36/int(np.abs(divisions)))

                if j==divisions:
                    j=0

                fringe_dir, pic_dir = projection_folders(i, data_folder, j, divisions)

                for shift in range(n_steps):
                    loca = fringe_create(shift, n_steps, nu0, X, xi0, Y, loca, fringe_dir)
                    fringe_convert(table, loca, fringe_dir)
                    project(fringe_dir, loca)
                    cap, picname = camera_setup(picname, exposur, cam_width, cam_height, portno)
                    photoshoot(cap, pic_dir, picname)

                    # Close everything
                    cap.release()
                    key=cv2.waitKey(2)
                    plt.close()
                    if key == 27:#if ESC is pressed, exit loop
                        cv2.destroyAllWindows()
                        break
    return nu00, nu1, divisions
def phaseshift(directory):
    """
    With an N-step fringe projection performed prior, outputting N number of
    webcam images in a directory, this function makes a phase shift map
    accordingly.
    """
    Iarr=np.array([])

    length=Image.open(directory+'/1-0.png').size[0] # gets length of exemplary webcam picture
    height=Image.open(directory+'/1-0.png').size[1] # gets height of exemplary webcam picture

    sin=np.zeros((height,length)) # prepares array to intake sin values
    cos=np.zeros((height,length)) # prepares array to intake cos values

    n=0
    N=len([name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))])
    N=int(N/5)
    for n in range (N): #for every step image in the directory

        I0=Image.open(directory+'/'+str(n+1)+'-0.png') # images are titled from 1 to N
        I1=Image.open(directory+'/'+str(n+1)+'-1.png')
        I2=Image.open(directory+'/'+str(n+1)+'-2.png')
        I3=Image.open(directory+'/'+str(n+1)+'-3.png')
        I4=Image.open(directory+'/'+str(n+1)+'-4.png')

        I=np.mean((np.asarray(I0),np.asarray(I1),np.asarray(I2),np.asarray(I3),np.asarray(I4)), axis=0)

        I=np.asarray(I, dtype='float32')
        sin=sin+I*np.sin(2*np.pi*n/N) # Critical math operation from page 27 of https://doi.org/10.1016/j.optlaseng.2018.04.019
        cos=cos+I*np.cos(2*np.pi*n/N) # Critical math operation from aforementioned paper
    phase = np.arctan2(cos,sin) # Critical math

    return phase

def unwrap(low, high, low_freq, high_freq):
    un=high+(2*np.pi)*np.around(((high_freq/low_freq)*low-high)/(2*np.pi))
    return un

def depthmap(u):
    u=(u-np.min(u))/(np.max(u)-np.min(u))
    return u

def graph(math, title, filepath):
    #plt.rcParams.update({'font.size': 20})
    plt.imshow(math, cmap='gray', interpolation='none')
    cbar=plt.colorbar()
    plt.title(title)
    plt.savefig(filepath)
    plt.close()

def xyz(u, title):
    m,n=u.shape
    R,C=np.mgrid[:m,:n]
    expression=np.column_stack((C.ravel(),R.ravel(), u.ravel()))
    np.savetxt(title, expression[:,:], delimiter=" ")

def intensity_cross_sctn(map, index, width, titl, filepath):
    #plt.rcParams.update({'font.size': 22})
    plt.plot(np.arange(width),map[int(index)])
    plt.title(titl)
    plt.savefig(filepath)
    plt.close()

def surface_plot(u, titl, filepath):
    #plt.rcParams.update({'font.size': 22})
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    X = np.arange(u.shape[0])
    Y = np.arange(u.shape[1])
    X, Y = np.meshgrid(X, Y)
    Z = u
    surf = ax.plot_surface(X, Y, Z.T, cmap=cm.coolwarm, linewidth=0, antialiased=False)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.title(titl)
    plt.savefig(filepath)
    plt.close()

def data_files(nu00, nu1, camera_to_projector_distance, to_wall_distance, divisions, folder):
    print('Prepare to input the four pixel corners of the meaningful part of the picture to crop to. Hit q when ready.')
    preview = mpimg.imread(folder+'/subject/0/high_pics/1-0.png')
    imgplot = plt.imshow(preview, cmap='gray')
    plt.show()


    z=input('Enter meaningful area to crop to, as in top_px,bottom_px,left_px,right_px: ')

    z=z.split(',')
    z=np.asarray(z, dtype='int')

    for a in range(divisions): # degree folders
        print('Making plots and mesh for position #'+str(a+1))
        deg_folder = a * int(360/divisions)

        dir=folder+'/wall/'+str(deg_folder)+'/plots_meshes'
        if os.path.exists(dir):
            shutil.rmtree(dir)
        os.makedirs(dir)

        dir=folder+'/subject/'+str(deg_folder)+'/plots_meshes'
        dir=folder+'/subject/'+str(deg_folder)+'/plots_meshes'
        if os.path.exists(dir):
            shutil.rmtree(dir)
        os.makedirs(dir)

        low_map=phaseshift(folder+'/wall/'+str(deg_folder)+'/low_pics')
        high_map=phaseshift(folder+'/wall/'+str(deg_folder)+'/high_pics')
        unwrapped_0=unwrap(low_map, high_map, nu00, nu1)

        graph(low_map, str(nu00)+' Frequency @ Wall', folder+'/wall/'+str(deg_folder)+'/plots_meshes/low_phase_map.png')
        graph(high_map, str(nu1)+' Frequency @ Wall', folder+'/wall/'+str(deg_folder)+'/plots_meshes/high_phase_map.png')
        graph(unwrapped_0, 'Unwrapped @ Wall', folder+'/wall/'+str(deg_folder)+'/plots_meshes/unwrapped_map.png')

        low_s_map=phaseshift(folder+'/subject/'+str(deg_folder)+'/low_pics')
        high_s_map=phaseshift(folder+'/subject/'+str(deg_folder)+'/high_pics')
        unwrapped=unwrap(low_s_map, high_s_map, nu00, nu1)
        depth=(int(to_wall_distance)/int(camera_to_projector_distance))*(unwrapped-unwrapped_0)

        graph(low_s_map, str(nu00)+' Frequency @ Subject', folder+'/subject/'+str(deg_folder)+'/plots_meshes/low_phase_map.png')
        graph(high_s_map, str(nu1)+' Frequency @ Subject', folder+'/subject/'+str(deg_folder)+'/plots_meshes/high_phase_map.png')
        graph(unwrapped, 'Unwrapped @ Wall', folder+'/subject/'+str(deg_folder)+'/plots_meshes/unwrapped_map.png')
        graph(depth, 'Depth Map', folder+'/subject/'+str(deg_folder)+'/plots_meshes/depth_map.png')
        depth=depth[z[0]:z[1],z[2]:z[3]]

        surface_plot(depth, 'Surface Plot of Subject', folder+'/subject/'+str(deg_folder)+'/plots_meshes/surface_plot.png')
        intensity_cross_sctn(depth, int(depth.shape[0]/4), z[3]-z[2], 'Cross Section 1/4-Way Down', folder+'/subject/'+str(deg_folder)+'/plots_meshes/cross_secction_quarter_down.png')
        intensity_cross_sctn(depth, int(depth.shape[0]/2), z[3]-z[2], 'Cross Section 1/2-Way Down', folder+'/subject/'+str(deg_folder)+'/plots_meshes/cross_section_half_down.png')
        intensity_cross_sctn(depth, int(3*depth.shape[0]/5), z[3]-z[2], 'Cross Section 3/5-Way Down', folder+'/subject/'+str(deg_folder)+'/plots_meshes/cross_section_three_fifth_down.png')
        xyz(-1*depth,folder+'/subject/'+str(deg_folder)+'/point_cloud.xyz')

if __name__ == "__main__":
    table=open_csv("projection_lookup_table.csv")

    folder='turn_fringe'

    portno=0
    exposur=40
    cam_width=1280
    cam_height=720

    # These 2 need to be in the same units. They're only used to form a ratio between the two
    camera_to_projector_distance=408
    to_wall_distance=552

    width, height = screen_res()
    nu00, nu1, divisions = procedure(folder, table, width, height, portno, exposur, cam_width, cam_height)

    data_files(nu00, nu1, camera_to_projector_distance, to_wall_distance, divisions, folder)
    #data_files(.25, 5, camera_to_projector_distance, to_wall_distance, 3, folder)
