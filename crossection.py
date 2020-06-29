"""
For calibration Plotting
"""
import numpy as np
import matplotlib.pyplot as plt
import cv2
import csv
import os,os.path
import scipy.interpolate as si

def old_sinusoid_test():
    img=cv2.imread('calibby/1.png')
    print(img[230][0])
    x=np.arange(img.shape[1])
    y=np.array([])
    for i in range (img.shape[1]):
        y=np.append(y,img[260][i][0])
    plt.plot(x,y)
    plt.xlabel('nth Pixel')
    plt.ylabel('Intensity')
    plt.title('Intensity of Cross-Section')
    plt.show()

def tbd():
    x=np.array([])
    y=np.array([])

    for z in range(int(255/10)+2):
        if z!=0:
            z=(z*10)-5
            myimg = cv2.imread('calib/'+str(z)+'.png')
            avg_color_per_row = np.average(myimg, axis=0)
            avg_color = np.average(avg_color_per_row, axis=0)
            x=np.append(x,z)
            y=np.append(y,avg_color[0])

    print(avg_color[0])
    plt.plot(x,y)
    axes = plt.gca()
    axes.set_xlim([0,255])
    axes.set_ylim([0,255])
    plt.xlabel('Projected Intensity')
    plt.ylabel('Average Captured Intensity')
    plt.title('Histogram of Input Image')
    plt.show()

def histogram_ranom_pixel():
    x=np.array([])
    y=np.array([])
    myimg = cv2.imread('calib/255.png')
    print(myimg.shape[0])
    print(myimg.shape[1])
    a=np.random.randint(myimg.shape[0])
    b=np.random.randint(myimg.shape[1])
    for z in range(int(255/10)+2):
        if z!=0:
            z=(z*10)-5
            myimg = cv2.imread('calib/'+str(z)+'.png')
            x=np.append(x,z)
            y=np.append(y,myimg[a][b][0])

    print(myimg[a][b][0])
    plt.plot(x,y)
    axes = plt.gca()
    axes.set_xlim([0,255])
    axes.set_ylim([0,255])
    plt.xlabel('Projected Intensity')
    plt.ylabel('Captured Intensity')
    plt.title('Histogram of Input Image @ Pixel ['+str(a)+' , '+str(b)+'] (10ms Exposure Time)')
    plt.show()

def calibration_obsolete():
    x=np.array([])
    y=np.array([])
    myimg = cv2.imread('calibfull/255.png')

    for z in range(256):
        if z!=0:
            myimg = cv2.imread('calibfull/'+str(z)+'.png')
            avg_color_per_row = np.average(myimg, axis=0)
            avg_color = np.average(avg_color_per_row, axis=0)
            x=np.append(x,z)
            y=np.append(y,avg_color[0])
            print(str(int(x[-1]))+','+str(int(y[-1])))

    rows = np.asarray(np.array([x,y]).T,dtype='int')
    # name of csv file
    filename = "plot.csv"
    # writing to csv file
    with open(filename, 'w') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

        # writing the data rows
        csvwriter.writerows(rows)

    plt.plot(x,y)
    axes = plt.gca()
    axes.set_xlim([0,255])
    axes.set_ylim([0,255])
    plt.xlabel('Projected Intensity')
    plt.ylabel('Average Captured Intensity')
    plt.title('Radiometric Calibration Curve for Input Image')# @ Pixel ['+str(a)+' , '+str(b)+'] (10ms Exposure Time)')
    plt.show()

def generate_csv_files():
    #ALPHA
    x=np.array([])
    y=np.array([])

    for z in range(1,256):
        x=np.append(x,z)
        average=np.array([])
        for i in range(5):
            myimg = cv2.imread('calib50/'+str(z)+'-'+str(i)+'.png')
            avg_color_per_row = np.average(myimg, axis=0)
            avg_color = np.average(avg_color_per_row, axis=0)
            average=np.append(average,avg_color[0])
            #or
            #average=np.append(average,myimg[540][960])
        y=np.append(y,np.average(average))
        print(str(int(x[-1]))+','+str(int(y[-1])))


    rows = np.asarray(np.array([x,y]).T,dtype='int')
    filename = "plot.csv"
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(rows)

    graph_info=np.genfromtxt('plot.csv', delimiter=',')
    x=(graph_info[:,[0]].T)[0]
    y=(graph_info[:,[1]].T)[0]

    x2=np.linspace(0, 255, num=18, endpoint=True)
    y2 = si.interp1d(x, y, kind='cubic',fill_value='extrapolate')
    y2=y2(x2)
    plt.plot(x,y,'o',x2,y2,'-')

    y2fine=np.array([])
    for n in range(len(x2)-1):
        y2f=np.asarray(np.around(np.linspace(y2[n],y2[n+1],num=16)),dtype='int')
        y2fine=np.append(y2fine,y2f[1:])
    rows = np.asarray(np.array([x,y2fine]).T,dtype='int')

    filename = "fitplot.csv"
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(rows)

    axes = plt.gca()
    axes.set_xlim([0,255])
    axes.set_ylim([0,255])
    plt.xlabel('Projected Intensity')
    plt.ylabel('Average Captured Intensity')
    plt.title('Radiometric Calibration Curve for Input Image')# @ Pixel ['+str(a)+' , '+str(b)+'] (10ms Exposure Time)')

    plt.show()
    #OMEGA

def find_the_middle():
    firstpic=cv2.imread('calibgradient/1-0.png')
    avg = np.average(firstpic, axis=0)
    darkrow=np.array([])
    for i in range(len(avg)):
        if avg[i][0]<.9:
            darkrow=np.append(darkrow,i)
    print(darkrow)
    nums = sorted(set(darkrow))
    gaps = [[s, e] for s, e in zip(nums, nums[1:]) if s+1 < e]
    edges = iter(nums[:1] + sum(gaps, []) + nums[-1:])
    consecutives=list(zip(edges, edges))

    print(consecutives)
    biggest=-1
    for consecutive in consecutives:
        if consecutive[1]-consecutive[0]>biggest:
            biggest=consecutive[1]-consecutive[0]
            biggest_idx=consecutive
    print(biggest)
    print(biggest_idx)
    the_middle=int((biggest_idx[0]+biggest_idx[1])/2)
    return the_middle

def middle_column_csv():
    middle=find_the_middle()

    x=np.array([])
    y=np.array([])

    for z in range(1,256):
        x=np.append(x,z)
        average=np.array([])
        for i in range(5):
            myimg = cv2.imread('calib50/'+str(z)+'-'+str(i)+'.png')
            average = np.average(myimg[:,middle], axis=0)
            #average=np.append(average,avg_color[0])
            #or
            #average=np.append(average,myimg[540][960])
        y=np.append(y,average[0])
        print(str(int(x[-1]))+','+str(int(y[-1])))


    rows = np.asarray(np.array([x,y]).T,dtype='int')
    filename = "plot.csv"
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(rows)

    graph_info=np.genfromtxt('plot.csv', delimiter=',')
    x=(graph_info[:,[0]].T)[0]
    y=(graph_info[:,[1]].T)[0]

    x2=np.linspace(0, 255, num=18, endpoint=True)
    y2 = si.interp1d(x, y, kind='cubic',fill_value='extrapolate')
    y2=y2(x2)
    plt.plot(x,y,'o',x2,y2,'-')

    y2fine=np.array([])
    for n in range(len(x2)-1):
        y2f=np.asarray(np.around(np.linspace(y2[n],y2[n+1],num=16)),dtype='int')
        y2fine=np.append(y2fine,y2f[1:])
    rows = np.asarray(np.array([x,y2fine]).T,dtype='int')

    filename = "fitplot.csv"
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(rows)

    axes = plt.gca()
    axes.set_xlim([0,255])
    axes.set_ylim([0,255])
    plt.xlabel('Projected Intensity')
    plt.ylabel('Average Captured Intensity')
    plt.title('Radiometric Calibration Curve for Input Image')# @ Pixel ['+str(a)+' , '+str(b)+'] (10ms Exposure Time)')

    plt.show()

def sinusoid_compare():
    directory='phaseimgs20/'
    N=len([name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))])
    x=np.arange(N)
    y1=np.array([])
    y2=np.array([])
    graph_info=np.genfromtxt('fitplot.csv', delimiter=',')

    for n in range (N):
        I1=cv2.imread(directory+str(n+1)+'.png')
        I2=cv2.imread('phasefringe/'+str(n+1)+'.png')
        y1=np.append(y1,I1[1224][1632][0])
        #print(np.where(graph_info[:,0]==I2[11][960][0])[0][0])
        """
        if I2[11][960][0]==0:
            I2[11][960][0]=1
        I2[11][960][0]=graph_info[np.where(graph_info[:,0]==I2[11][960][0])[0][0]][1]
        """
        y2=np.append(y2,I2[11][960][0])

    fig, ax = plt.subplots()
    ax.plot(x+1, y1, '-b', label='Captured')
    ax.plot(x+1, y2, '-r', label='Projected')
    leg = ax.legend()

    plt.xlabel('n Step')
    plt.xticks(np.arange(1,N+1))
    plt.ylabel('Captured Intensity @ Pixel')
    plt.title('Captured Intensity @ Middle Pixel')
    plt.show()

def sinusoid_compare_quick():
    I1=cv2.imread('fringe.png')
    I2=cv2.imread('wah.png')

    fig, ax = plt.subplots()
    ax.plot(np.arange(1920), I1[540], '-b', label='Captured')
    ax.plot(np.arange(3264), I2[1224], '-r', label='Projected')
    leg = ax.legend()

    plt.xlabel('n Step')
    plt.ylabel('Captured Intensity @ Specified Pixel')
    plt.title('Captured Intensity @ Pixel [25][1632]')
    plt.show()

if __name__ == "__main__":
    #sinusoid_compare()
    generate_csv_files()
    #middle_column_csv()
