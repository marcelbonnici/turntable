import matplotlib
matplotlib.use('tkagg')
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib import cm
from matplotlib.ticker import Linearphase_numtor, FormatStrFormatter
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
    '''
    Used to open CSV files as an alternative to numpy genfromtxt

    directory - Where CSV file is

    Returns:
    CSV file as 2D matrix
    '''
    results = []
    with open(directory) as csvfile:
        reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC) # change contents to floats
        for row in reader: # each row is a list
            results.append(row)
    return np.asarray(results)

def lookup(table, desired_captured_intensity):
    '''
    Modifies sinusoidal fringe pattern to intensities ideal for the camera
    Ex: if projected intensity of 70 is captured as 65, and projected 75 is
        captured as 70, then change all pixels of 70 in original sinusoid to 75

    table - Lookup table
    desired_captured_intensity - grayscale intensity code wants cam to perceive

    Returns:
    grayscale intensity code must project to be perceived ideally by camera
    '''
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



def lookup_pixel(table, desired_captured_intensity, height):
    '''
    Alternative method for pixel-by-pixel calibration; yielded subpar fringes before project deadline

    table - lookup table
    desired_captured_intensity - grayscale intensity code wants cam to perceive
    height - height of pixel in captured image

    Returns:
    grayscale intensity code must project to be perceived ideally by camera
    '''
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
    '''
    Finds width and height of monitor for full screen projections

    Returns:
    width, height - Resolution of monitor/projector
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

def user_input():
    '''
    Take user's parameters to display fringes and rotate turntable accordingly

    Returns:
    n_steps - How many times to portray the same sinusoidal frequency at the
                same artifact pose, with different phase shifts
    divisions - Quantity of angles artifact is photographed at
    low_period_x - number of periods the smaller frequency will be, horizontally
    low_period_y - number of periods the smaller frequency will be, vertictally
    high_period_x - number of periods the bigger frequency will be, horizontally
    high_period_y - number of periods the bigger frequency will be, vertictally
    '''
    n_steps=int(input('Number of Steps: '))
    divisions = int(input('Number of Fractions of Rotations: '))
    low_period_x=input('Enter a LOW number of periods along x-axis: ') #Must be<=1
    try:
        low_period_x=float(low_period_x)
    except ValueError:
        low_period_x=0.25
    if low_period_x > 1:
        low_period_x=0.25

    # Was not reached but something like: float(input('Enter a LOW number of periods along y-axis: '))
    low_period_y=0

    if low_period_x>0:
        low_period_x=2*np.pi/(1/low_period_x)
    if low_period_y>0:
        low_period_y=2*np.pi/(1/low_period_y)

    high_period_x=input('Enter a HIGH number of periods along x-axis: ')
    try:
        high_period_x=float(high_period_x)
    except ValueError:
        high_period_x=0.25
    if high_period_x<=1:
        high_period_x=5
    high_period_y=0 # Was not reached but something like: float(input('Enter a HIGH number of periods along y-axis: '))
    if high_period_x>0:
        high_period_x=2*np.pi/(1/high_period_x)
    if high_period_y>0:
        high_period_y=2*np.pi/(1/high_period_y)

    return n_steps, divisions, low_period_x, low_period_y, high_period_x, high_period_y

def fringe_create(shift, n_steps, period_x, X, period_y, Y, phase_num, fringe_dir):
    '''
    Makes a mathematically perfect fringe, to be calibrated for the camera after

    shift - iterator of n_steps
    n_steps - # of different phase shifts to project a sinusoidal frequency at
    period_x - Horizontal period of sinusoidal projection
    X - Meshgrid spanning from grayscale 50 to 240 in each of the rows
    period_y - Vertical period of sinusoidal projection
    Y - Meshgrid spanning from grayscale 50 to 240 in each of the columns
    phase_num - File name of pattern. Also iterator of n_steps, starting with 1
    fringe_dir - Where generated fringe patterns are exported

    Return:
    phase_num
    '''
    shift=shift*2*np.pi/n_steps
    img=(np.cos(period_x*X+period_y*Y-shift-0*np.pi/2)/2+0.5)*190+50
    #eliminates noise floor and ceiling in cameras (50 to 240)

    img=img/255
    img[-1][-1]=0 #image wants to push minimum value (50/255) to total darkness, so I made this negligible pixel zero to prevent compromising other pixels
    img[-2][-1]=1 #instead of pushing maximum value (240/255) to 1, I made a negligible pixel 1 to represent 255/255
    phase_num=phase_num+1
    plt.imsave(fringe_dir+'/'+str(phase_num)+'.png',img, cmap='gray')
    return phase_num

def fringe_convert(table, phase_num, fringe_dir):
    '''
    The process bridging the mathematically perfect sinusoid to the lookup table

    table - File comparing the projected to the perceived (by camera) intensity
    phase_num - File name of pattern
    fringe_dir - Where generated fringe patterns are exported
    '''
    img = mpimg.imread(fringe_dir+'/'+str(phase_num)+'.png')
    for j in range (img.shape[1]): #for every pixel in img's row
        desired_captured_intensity=img[0,j,0]
        projected_loc=lookup(table, np.around(255*desired_captured_intensity))
        img[:,j]=np.asarray([projected_loc/255,projected_loc/255,projected_loc/255,1])
    img[-1][-1]=0
    img[-2][-1]=0
    plt.imsave(fringe_dir+'/'+str(phase_num)+'.png',img,cmap='gray')

def project (fringe_dir, phase_num):
    '''
    Puts calibrated pattern on the projector
    fringe_dir - File location to import projected pattern from
    phase_num - File name of pattern
    '''
    image = mpimg.imread(fringe_dir+'/'+str(phase_num)+'.png')
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
    '''
    Prepares camera's parameters
    picname - Phase number, contributing to photograph's names
    exposur - Camera value found to noise floor & ceiling with projections
    cam_width, cam_height - camera's image resolution
    portno - Computer port where camera is connected

    Returns:
    cap - Camera ready for image capturing
    picname - picname, increase for next phase_shift
    '''
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
    '''
    Takes 5 images at each fringe, minimizing artifacts' influence

    cap - Camera stream
    pic_dir - where photographs are exported to
    picname - phase shift number in file name
    '''
    k=0
    while(k<=6):
        ret, frame = cap.read()
        if k>1:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(pic_dir+'/'+str(picname)+'-'+str(k-2)+'.png',gray)
        k=k+1

def make_folders(data_folder, divisions):
    '''
    Make folders for poses the artifact is pictured at (For 4: 0, 90, 180, 270)
    '''
    for m in range(divisions):
        deg_folder = m * int(360/divisions)
        folder = str(data_folder)+'/'+str(deg_folder)
        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.makedirs(folder)

def toggle_low_high(i, low_period_x, low_period_y, high_period_x, high_period_y, data_folder, deg_folder):
    '''
    Changes between high and low frequency values for determining fringe pattern
    and make the directories for each

    i - Indicates if low or high frequency projections are next to project
    low_period_x - User input < 1
    low_period_y - Set to 0
    high_period_x - User input  > 1
    high_period_y - Set to 0
    data_folder - Folder for all data w/o artifact, or for all data w/ artifact
    deg_folder - Sub-folder of data_folder, specific to the turntable pose

    Returns:
    period_y - Either low or high
    period_x - Either low or high
    pic_dir - Where low, or high, frequency patterns on object pics are stored
    fringe_dir - Where low, or high, frequency fringe patterns are stored
    '''
    if i == 1: #Changes between projecting low frequency and high frequency
        period_x=high_period_x
        period_y=high_period_y

        pic_dir=data_folder+'/'+str(deg_folder)+'/high_pics'
        if os.path.exists(pic_dir):
            shutil.rmtree(pic_dir)
        os.makedirs(pic_dir)

        fringe_dir=data_folder+'/'+str(deg_folder)+'/high_fringe'
        if os.path.exists(fringe_dir):
            shutil.rmtree(fringe_dir)
        os.makedirs(fringe_dir)
    else:
        period_x=low_period_x
        period_y=low_period_y

        pic_dir=data_folder+'/'+str(deg_folder)+'/low_pics'
        if os.path.exists(pic_dir):
            shutil.rmtree(pic_dir)
        os.makedirs(pic_dir)

        fringe_dir=data_folder+'/'+str(deg_folder)+'/low_fringe'
        if os.path.exists(fringe_dir):
            shutil.rmtree(fringe_dir)
        os.makedirs(fringe_dir)

    return period_y, period_x, pic_dir, fringe_dir

def projection_folders(i, data_folder, j, divisions):
    '''
    Choose whether the directories of interest are for low of high frequency

    i - Indicates if low or high frequency projections are next to project
    data_folder - Folder for all data w/o artifact, or for all data w/ artifact
    divisions - How many equal slices a rotation to photograph artifact at

    Returns:
    pic_dir - Where low, or high, frequency patterns on object pics are stored
    fringe_dir - Where low, or high, frequency fringe patterns are stored
    '''
    if i == 1:
        fringe_dir=data_folder+'/'+str(j*int(360/divisions))+'/high_fringe'
        pic_dir=data_folder+'/'+str(j*int(360/divisions))+'/high_pics'
    else:
        fringe_dir=data_folder+'/'+str(j*int(360/divisions))+'/low_fringe'
        pic_dir=data_folder+'/'+str(j*int(360/divisions))+'/low_pics'
    return fringe_dir, pic_dir

def gather_data(folder, table, width, height, portno, exposur, cam_width, cam_height):
    '''
    Rotates turntable, projects sinusoidal patterns on subject & photographs it.

    folder - Where all data will be exported to
    table - Data that influences projected patterns WRT camera properties
    width, height - Resolution of monitor/projector
    portno - Computer port where camera is connected
    exposur - Camera value found to noise floor & ceiling with projections
    cam_width, cam_height - camera's image resolution

    Returns:
    low_period_x - number of periods the smaller frequency will be, horizontally
    high_period_x - number of periods the bigger frequency will be, horizontally
    divisions - Quantity of angles artifact is photographed at
    '''
    #Sets camera exposure to manual, not overriding influence of 'exposur'
    subprocess.call(['v4l2-ctl','-d',str(portno),'--set-ctrl=exposure_auto=1'])
    x=np.linspace(0,1,width)
    y=np.linspace(0,1,height)
    X,Y=np.meshgrid(x,y)

    n_steps, divisions, low_period_x, low_period_y, high_period_x, high_period_y = user_input()

    for q in range(2): #Takes photos without, then with, artifact on display
        if q==0:
            data_folder=folder+'/wall'
            input("Clear off turntable. Press Enter to continue.")
        else:
            data_folder=folder+'/subject'
            input("Place object on turntable. Press Enter to continue.")

        make_folders(data_folder, divisions)

        for i in range(2): #low frequency, then high frequency
            for p in range (divisions):
                deg_folder = p * int(360/divisions)
                period_y, period_x, pic_dir, fringe_dir = toggle_low_high(i, low_period_x, low_period_y, high_period_x, high_period_y, data_folder, deg_folder)

            for j in range(1,divisions+1): #For each turntable pose
                phase_num=0
                picname=0

                #if divisions > 1:
                turn.degrees(360/divisions)
                time.sleep(36/int(np.abs(divisions)))

                if j==divisions:
                    j=0 #Used to treat 1 rotation as reaching 0 degrees, not 360

                fringe_dir, pic_dir = projection_folders(i, data_folder, j, divisions)

                for shift in range(n_steps):
                    phase_num = fringe_create(shift, n_steps, period_x, X, period_y, Y, phase_num, fringe_dir)
                    fringe_convert(table, phase_num, fringe_dir)
                    project(fringe_dir, phase_num)
                    cap, picname = camera_setup(picname, exposur, cam_width, cam_height, portno)
                    photoshoot(cap, pic_dir, picname)

                    # Close everything
                    cap.release()
                    key=cv2.waitKey(2)
                    plt.close()
                    if key == 27:#if ESC is pressed, exit loop
                        cv2.destroyAllWindows()
                        break
    return low_period_x, high_period_x, divisions

def phaseshift(directory):
    '''
    With an N-step fringe projection performed prior, outputting N number of
    webcam images in a directory, this function makes a phase shift map
    accordingly.

    directory - Folder sotring photographs

    Returns:
    phase - Phase map, for either low/high frequency with(out) artifact on table
    '''
    Iarr=np.array([])

    length=Image.open(directory+'/1-0.png').size[0] # gets length of exemplary webcam picture
    height=Image.open(directory+'/1-0.png').size[1] # gets height of exemplary webcam picture

    sin=np.zeros((height,length)) # prepares array to intake sin values
    cos=np.zeros((height,length)) # prepares array to intake cos values

    n=0
    N=len([name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))])
    N=int(N/5) # N is number of phase shifts
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
    '''
    Minimizes high frequency phase map's wrapping artifacts by merging it with
    the low map

    low - low map
    high - high map
    low_freq - User-inputted low frequency, which is <1
    high_freq - User-inputted high frequency, which is >1

    Returns:
    un - Unwrapped map
    '''
    un=high+(2*np.pi)*np.around(((high_freq/low_freq)*low-high)/(2*np.pi))
    return un

def depthmap(to_wall_distance, camera_to_projector_distance, unwrapped, unwrapped_0):
    '''
    Disparity between unwrapped map with and without subject on table

    camera_to_projector_distance - Dist from projector lens to camera lens mount
    to_wall_distance - Dist between the camera & projector to end of turntable
    unwrapped - Unwrapped map with artifact
    unwrapped_0 - Unwrapped map without artifact

    Returns:
    depth__map - Depth map
    '''
    u=(int(to_wall_distance)/int(camera_to_projector_distance))*(unwrapped-unwrapped_0)
    return depth__map

def graph(math, title, filepath):
    '''
    Clean way to plot the data

    math - phase map
    title - map title
    filepath - Where map is exported
    '''
    plt.imshow(math, cmap='gray', interpolation='none')
    cbar=plt.colorbar()
    plt.title(title)
    plt.savefig(filepath)
    plt.close()

def xyz(depth_map, title):
    '''
    Converts depth map into point cloud depth and xyz format
    '''
    m,n=u.shape
    R,C=np.mgrid[:m,:n]
    expression=np.column_stack((C.ravel(),R.ravel(), u.ravel()))
    np.savetxt(title, expression[:,:], delimiter=" ")

def intensity_cross_sctn(map, index, width, titl, filepath):
    '''
    Cross section at certain row in depth map, to forecast curvature of wall
    '''
    #plt.rcParams.update({'font.size': 22})
    plt.plot(np.arange(width),map[int(index)])
    plt.title(titl)
    plt.savefig(filepath)
    plt.close()

def surface_plot(depth_map, titl, filepath):
    '''
    Makes a 3D surface plot; similar to creating a point cloud but in python
    '''
    #plt.rcParams.update({'font.size': 22})
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    X = np.arange(u.shape[0])
    Y = np.arange(u.shape[1])
    X, Y = np.meshgrid(X, Y)
    Z = depth_map
    surf = ax.plot_surface(X, Y, Z.T, cmap=cm.coolwarm, linewidth=0, antialiased=False)
    ax.zaxis.set_major_phase_numtor(Linearphase_numtor(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.title(titl)
    plt.savefig(filepath)
    plt.close()

def graph_export_data(low_period_x, high_period_x, camera_to_projector_distance, to_wall_distance, divisions, folder):
    '''
    Organizes converting camera's images into plots

    low_period_x - number of periods the smaller frequency will be, horizontally
    high_period_x - number of periods the bigger frequency will be, horizontally
    camera_to_projector_distance - Dist from projector lens to camera lens mount
    to_wall_distance - Dist between the camera & projector to end of turntable
    divisions - Quantity of angles artifact is photographed at
    folder - Where all data will be exported to
    '''
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
        unwrapped_0=unwrap(low_map, high_map, low_period_x, high_period_x)

        graph(low_map, 'LOW Frequency @ Wall', folder+'/wall/'+str(deg_folder)+'/plots_meshes/low_phase_map.png')
        graph(high_map, 'HIGH Frequency @ Wall', folder+'/wall/'+str(deg_folder)+'/plots_meshes/high_phase_map.png')
        graph(unwrapped_0, 'Unwrapped @ Wall', folder+'/wall/'+str(deg_folder)+'/plots_meshes/unwrapped_map.png')

        low_s_map=phaseshift(folder+'/subject/'+str(deg_folder)+'/low_pics')
        high_s_map=phaseshift(folder+'/subject/'+str(deg_folder)+'/high_pics')
        unwrapped=unwrap(low_s_map, high_s_map, low_period_x, high_period_x)
        depth=(int(to_wall_distance)/int(camera_to_projector_distance))*(unwrapped-unwrapped_0)

        graph(low_s_map, 'LOW Frequency @ Subject', folder+'/subject/'+str(deg_folder)+'/plots_meshes/low_phase_map.png')
        graph(high_s_map, 'HIGH Frequency @ Subject', folder+'/subject/'+str(deg_folder)+'/plots_meshes/high_phase_map.png')
        graph(unwrapped, 'Unwrapped @ Subject', folder+'/subject/'+str(deg_folder)+'/plots_meshes/unwrapped_map.png')
        graph(depth, 'Depth Map', folder+'/subject/'+str(deg_folder)+'/plots_meshes/depth_map.png')
        graph(low_s_map-low_map, 'Disparity of Low Frequency', folder+'/subject/'+str(deg_folder)+'/plots_meshes/low_disparity_map.png')
        depth=depth[z[0]:z[1],z[2]:z[3]]

        surface_plot(depth, 'Surface Plot of Subject', folder+'/subject/'+str(deg_folder)+'/plots_meshes/surface_plot.png')
        intensity_cross_sctn(depth, int(depth.shape[0]/4), z[3]-z[2], 'Cross Section 1/4-Way Down', folder+'/subject/'+str(deg_folder)+'/plots_meshes/cross_secction_quarter_down.png')
        intensity_cross_sctn(depth, int(depth.shape[0]/2), z[3]-z[2], 'Cross Section 1/2-Way Down', folder+'/subject/'+str(deg_folder)+'/plots_meshes/cross_section_half_down.png')
        intensity_cross_sctn(depth, int(3*depth.shape[0]/5), z[3]-z[2], 'Cross Section 3/5-Way Down', folder+'/subject/'+str(deg_folder)+'/plots_meshes/cross_section_three_fifth_down.png')
        xyz(-1*depth,folder+'/subject/'+str(deg_folder)+'/point_cloud.xyz')
        xyz((low_s_map-low_map)[z[0]:z[1],z[2]:z[3]],folder+'/subject/'+str(deg_folder)+'/low_point_cloud.xyz')

if __name__ == "__main__":
    '''
    Designate file export and camera settings before starting the program

    table - Data that influences projected patterns WRT camera properties
    folder - Where all data will be exported to
    camera_to_projector_distance - Dist from projector lens to camera lens mount
    to_wall_distance - Dist between the camera & projector to end of turntable
    cam_width, cam_height - camera's image resolution
    portno - Computer port where camera is connected
    exposur - Camera value found to noise floor & ceiling with projections
    (Found in GH README "Part 1")
    '''
    table=open_csv("projection_lookup_table.csv")
    folder='fringe_subject'

    # These 2 need to be in the same units. They're only used to form a ratio
    camera_to_projector_distance=112
    to_wall_distance=552

    cam_width=1280
    cam_height=720
    portno=0
    exposur=40

    width, height = screen_res()
    low_period_x, high_period_x, divisions = gather_data(folder, table, width, height, portno, exposur, cam_width, cam_height)

    graph_export_data(low_period_x, high_period_x, camera_to_projector_distance, to_wall_distance, divisions, folder)
    #graph_export_data(.5,30, camera_to_projector_distance, to_wall_distance, 1, folder)
