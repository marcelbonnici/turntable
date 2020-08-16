"""
For calibration Plotting
"""
import numpy as np
import matplotlib.pyplot as plt
import cv2
import csv
import os,os.path
import scipy.interpolate as si
from scipy.interpolate import UnivariateSpline
import numpy.polynomial.polynomial as poly

def polyfit_calibrate():
    """
    Takes a 1-to-1 plot of each projected to captured intensity and makes it a polyfit line
    """
    graph_info=np.genfromtxt('lplot.csv', delimiter=',')
    x=(graph_info[:,[0]].T)[0]
    y=(graph_info[:,[1]].T)[0]

    f=0
    while y[f]==0:
        f=f+1

    c=254
    while y[c]>=246:
        c=c-1

    z=np.polyfit(x[f:c],y[f:c],11)
    p=np.poly1d(z)
    xp=np.linspace(x[0],x[-1], num=255)
    p=p(xp[f:c])
    yp=np.concatenate((y[0:f],p,y[c:]), axis=0)

    rows = np.asarray(np.array([xp,yp]).T,dtype='int')

    filename = "lfitplot.csv"
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(rows)

    fig, ax = plt.subplots()
    ax.plot(x, y, '-b', label='Before Line Fitting')
    ax.plot(xp, yp, '-r', label='After Line Fitting')
    leg = ax.legend()

    ax.set_xlim([0,255])
    ax.set_ylim([0,255])
    plt.xlabel('Projected Intensity', fontsize=18)
    plt.ylabel('Average Captured Intensity', fontsize=18)
    plt.title('Radiometric Calibration Curve for Input Image', fontsize=18)# @ Pixel ['+str(a)+' , '+str(b)+'] (10ms Exposure Time)')
    plt.show()

def basic_calibrate():
    """
    Averages all images at a shared, projected intensity to map the average pixel intensity to the projected intensity
    """
    x=np.array([])
    y=np.array([])

    for z in range(1,256):
        x=np.append(x,z)
        average=np.array([])
        for i in range(5):
            myimg = cv2.imread('lcalibgradient/'+str(z)+'-'+str(i)+'.png')
            avg_color= np.average(myimg[:,int(myimg.shape[1]/2)])
            #avg_color = np.average(avg_color_per_row, axis=0)
            average=np.append(average,avg_color)
        y=np.append(y,np.average(average))
        print(str(int(x[-1]))+','+str(int(y[-1])))

    rows = np.asarray(np.array([x,y]).T,dtype='int')
    filename = "lplot.csv" #CHANGED
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(rows)

def gradient_calibrate():
    """
    Compares a projected gradient image to the capture of the projection on a white wall, making a lookup csv with the best results
    """
    plt.rcParams.update({'font.size': 22})
    basis=cv2.imread('lbasis.png')[540,int(1920/2):]
    sample=cv2.imread('lcalibgradient/51-0.png')

    sample=np.mean(sample, axis=0)

    sample=sample[int(sample.shape[0]/2):]
    cherries=np.array([])
    slength=int(sample.shape[0])
    blength=int(basis.shape[0])

    for n in range(blength):
        proj=basis[n,0]
        capt=sample[int(slength/blength*n),0] # 1.7 CHANGED

        if n==0:
            old=proj
            sum=0
            tally=0
        if proj!=old:
            cherries=np.append(cherries, [old, int(sum/tally)])#print(str(old)+","+str(int(sum/tally)))
            sum=0
            tally=0
        if n==int(np.around(blength)-1):
            cherries=np.append(cherries, [old, int(sum/tally)])#print(str(proj)+","+str(int(sum/tally)))

        sum=sum+capt
        tally=tally+1
        old=proj

    cherries=cherries.reshape(int(len(cherries)/2),2)
    cherriesT=cherries.T

    x=cherriesT[0]
    y=cherriesT[1]
    print(cherriesT)
    z=np.polyfit(x,y,11)
    p=np.poly1d(z)
    xp=np.linspace(x,y, num=191)
    p=p(xp)
    yp=p

    rows = np.asarray(np.array([xp,yp]).T,dtype='int')[:,0]
    rows=rows[int(np.where(rows[:,0]==50)[0][0]):]
    np.savetxt("lcherrypick.csv", rows, delimiter=",", fmt='%d')
    fig, ax = plt.subplots()
    ax.plot(x, y, '-b', label='Before Line Fitting')
    ax.plot(xp, yp, '-r', label='After Line Fitting')
    leg = ax.legend()

    ax.set_xlim([50,241])
    ax.set_ylim([0,260])
    plt.xlabel('Projected Intensity', fontsize=18)
    plt.ylabel('Captured Intensity', fontsize=18)
    plt.title('Radiometric Calibration Curve for Input Image', fontsize=18)# @ Pixel ['+str(a)+' , '+str(b)+'] (10ms Exposure Time)')
    plt.show()

def gradient_calibrate_new():
    """
    Compares a projected gradient image to the capture of the projection on a white wall, making a lookup csv with the best results
    """
    plt.rcParams.update({'font.size': 22})
    basis=cv2.imread('lbasis.png')[540,int(1920/2):]

    sample=np.array([])
    for i in range(50, 256):
        intensity_avg=np.array([])
        for j in range(1, 5):
            pic=cv2.imread('lcalibgradient/'+str(i)+'-'+str(j)+'.png')
            pic=np.mean(pic[:,int(pic.shape[1]/2)])
            intensity_avg=np.append(intensity_avg, pic)
        intensity_avg=np.mean(intensity_avg)
        sample=np.append(sample,intensity_avg)
    #sample=np.mean(sample, axis=0)
    #print(sample)
    #sample=sample[int(sample.shape[0]/2):]
    cherries=np.array([])
    slength=int(sample.shape[0])
    blength=int(basis.shape[0])
    """
    for n in range(blength):
        proj=basis[n,0]
        capt=sample[int(slength/blength*n)] # 1.7 CHANGED

        if n==0:
            old=proj
            sum=0
            tally=0
        if proj!=old:
            cherries=np.append(cherries, [old, int(sum/tally)])#print(str(old)+","+str(int(sum/tally)))
            sum=0
            tally=0
        if n==int(np.around(blength)-1):
            cherries=np.append(cherries, [old, int(sum/tally)])#print(str(proj)+","+str(int(sum/tally)))

        sum=sum+capt
        tally=tally+1
        old=proj

    cherries=cherries.reshape(int(len(cherries)/2),2)
    cherriesT=cherries.T
    """
    #x=cherriesT[0]
    #y=cherriesT[1]
    x=np.arange(50,241)
    y=sample[:-15]
    z=np.polyfit(x,y,11)
    p=np.poly1d(z)
    xp=np.linspace(x,y, num=191)
    p=p(xp)
    yp=p
    rows = np.asarray(np.array([xp,yp]).T,dtype='int')[:,0]
    rows=rows[int(np.where(rows[:,0]==50)[0][0]):]
    np.savetxt("lcherrypick.csv", rows, delimiter=",", fmt='%d')
    fig, ax = plt.subplots()
    ax.plot(x, y, '-b', label='Before Line Fitting')
    ax.plot(xp, yp, '-r', label='After Line Fitting')
    leg = ax.legend()

    ax.set_xlim([50,241])
    ax.set_ylim([0,260])
    plt.xlabel('Projected Intensity', fontsize=18)
    plt.ylabel('Captured Intensity', fontsize=18)
    plt.title('Radiometric Calibration Curve for Input Image', fontsize=18)# @ Pixel ['+str(a)+' , '+str(b)+'] (10ms Exposure Time)')
    plt.show()

def three_cross_section():
    """
    Compares the ideal sinusoid to the calibrated sinusoid to the captured, gradient sinusoid
    """
    plt.rcParams.update({'font.size': 22})

    perfect=cv2.imread('sinusoid.png')[100,:,0]
    transformed=cv2.imread('lphasefringe/1.png')[100,:,0]
    observed=cv2.imread('steppics/1.png')
    #[155:-155,280:-210]
    observed=observed[int(observed.shape[0]/2),280:-210,0]#observed[1224,150:-150,0]
    observe=np.array([])
    ratio=len(observed)/len(transformed)
    print(ratio)
    for i in range(int(observed.shape[0]/ratio)):
        observe=np.append(observe,observed[int(ratio*i)])

    #plt.plot(np.arange(1,1921),perfect, '-r', np.arange(1,1921),transformed, '-g', np.arange(len(observe)), observe, '-b')

    fig, ax = plt.subplots()
    ax.plot(np.arange(1,1921),perfect, '-r', label='Perfect Sinusoid')
    ax.plot(np.arange(1,1921),transformed, '-g', label='Transformed Sinusoid')
    ax.plot(np.arange(len(observe)), observe, '-b', label = 'Observed Sinusoid')
    leg = ax.legend()

    plt.xlabel('Pixel # (Horizontally)')
    plt.ylabel('Captured Intensity @ Pixel')
    plt.title('Captured Intensity @ Middle Row')
    plt.show()

if __name__ == "__main__":

    #basic_calibrate()

    #gradient_calibrate()

    #polyfit_calibrate()

    #three_cross_section()

    gradient_calibrate_new()
