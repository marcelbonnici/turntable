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
    for i in range(1, 256): #was 50, 256
        intensity_avg=np.array([])
        for j in range(5):
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

    #x=cherriesT[0]
    #y=cherriesT[1]
    x=np.arange(1,256)# was 50,241
    y=sample#was sample[:-15]
    z=np.polyfit(x,y,11)
    p=np.poly1d(z)
    xp=np.linspace(x,y, num=255)#was 191
    p=p(xp)
    yp=p
    rows = np.asarray(np.array([xp,yp]).T,dtype='int')[:,0]
    rows=rows[int(np.where(rows[:,0]==1)[0][0]):] #Formerly where == 50
    np.savetxt("lcherrypick.csv", rows, delimiter=",", fmt='%d')
    fig, ax = plt.subplots()
    ax.plot(x, y, '-b', label='Before Line Fitting')
    ax.plot(xp, yp, '-r', label='After Line Fitting')
    leg = ax.legend()

    plt.xlabel('Projected Intensity', fontsize=18)
    plt.ylabel('Captured Intensity', fontsize=18)
    plt.title('Radiometric Calibration Curve for Input Image', fontsize=18)# @ Pixel ['+str(a)+' , '+str(b)+'] (10ms Exposure Time)')
    plt.show()

def gradient_calibrate_pixel():
    """
    Compares a projected gradient image to the capture of the projection on a white wall, making a lookup csv with the best results
    """
    plt.rcParams.update({'font.size': 22})
    basis=cv2.imread('lbasis.png')[540,int(1920/2):]

    all_intensities=np.array([])

    for i in range(1, 256): #was 256
        print(i)
        full_row=np.array([])

        pic0=cv2.imread('lcalibgradient/'+str(i)+'-0.png')
        pic1=cv2.imread('lcalibgradient/'+str(i)+'-1.png')
        pic2=cv2.imread('lcalibgradient/'+str(i)+'-2.png')
        pic3=cv2.imread('lcalibgradient/'+str(i)+'-3.png')
        pic4=cv2.imread('lcalibgradient/'+str(i)+'-4.png')

        pic0=pic0[:,int(pic0.shape[1]/2),0]
        pic1=pic1[:,int(pic1.shape[1]/2),0]
        pic2=pic2[:,int(pic2.shape[1]/2),0]
        pic3=pic3[:,int(pic3.shape[1]/2),0]
        pic4=pic4[:,int(pic4.shape[1]/2),0]

        column=np.mean((pic0,pic1,pic2,pic3,pic4), axis=0)

        all_intensities=np.append(all_intensities, column)

    all_intensities=np.reshape(all_intensities, (255,340))
    all_intensities=np.asarray(all_intensities, dtype='int')

    x=np.arange(1,256)

    for n in range(all_intensities.shape[1]):
        y=all_intensities[:,n] # random value for checking
        z=np.polyfit(x,y,11)
        p=np.poly1d(z)
        xp=np.linspace(x,y, num=255)
        p=p(xp)
        yp=p

        rows = np.asarray(np.array([xp,yp]).T,dtype='int')[:,0]
        rows=rows[int(np.where(rows[:,0]==1)[0][0]):]

        if n==0:
            actual_rows=rows.T
        else:
            rows=rows[:,1]
            actual_rows=np.append(actual_rows,rows)
        print('n='+str(n))

    actual_rows=np.reshape(actual_rows, (341,255))
    actual_rows=actual_rows.T
    np.savetxt("pixelcalibrate.csv", actual_rows, delimiter=",", fmt='%d')
    """
    fig, ax = plt.subplots()
    ax.plot(x, y, '-b', label='Before Line Fitting')
    ax.plot(x, actual_rows[:,200], '-r', label='After Line Fitting')
    leg = ax.legend()

    plt.xlabel('Projected Intensity', fontsize=18)
    plt.ylabel('Captured Intensity', fontsize=18)
    plt.title('Radiometric Calibration Curve for Input Image', fontsize=18)# @ Pixel ['+str(a)+' , '+str(b)+'] (10ms Exposure Time)')
    plt.show()
    """
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

def three_cross_section_new():
    plt.rcParams.update({'font.size': 18})
    directory='sinusoid_avg/'#'lphaseimgs20/'
    N=len([name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))])
    x=np.arange(N)
    y3=np.array([])#transformed

    region=320

    if str(cv2.imread(directory+'1-0.png')) != 'None':
        print('avg')
        y1=average_images_together(directory, region) #observed
        N=int(N/5)
    else:
        print('not_avg')
        y1=bring_images_together(directory, region) #observed

    for n in range (N):
        I3=cv2.imread('lphasefringe/'+str(n+1)+'.png')
        y3=np.append(y3,I3[540][int(I3.shape[1]/2)][0])


    y2=np.array([50,55,68,89,116,145,174,201,222,235,240,235,222,201,174,145,116,89,68,55])
    fig, ax = plt.subplots()

    ax.plot([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20], y2, '-r', label='Perfect Sinusoid')
    ax.plot([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20], y3, '-g', label='Transformed Sinusoid')
    ax.plot([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20], y1, '-b', label='Observed Sinusoid')

    leg = ax.legend()

    plt.xlabel('n Step')
    plt.xticks(np.arange(1,N+1))
    plt.ylabel('Captured Intensity @ Random Vertical Pixel')
    plt.title('Captured Intensity 1/2-Way Down Image')
    plt.show()

def bring_images_together(directory, region):

    N=len([name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))])
    y1=np.array([]) #observed

    for n in range (N):
        I1=cv2.imread(directory+str(n+1)+'.png')
        y1=np.append(y1,I1[int(region),int(I1.shape[1]/2),0])

    return y1

def average_images_together(directory, region):

    N=len([name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))])

    intensity=np.array([])

    for n in range (int(N/5)):
        p=0
        pixel_intensity=np.array([])
        photo=cv2.imread(directory+str(n+1)+'-'+str(p)+'.png')

        while str(photo) != 'None':
            pixel_intensity=np.append(pixel_intensity,photo[int(region),int(photo.shape[1]/2),0])
            p=p+1
            photo=cv2.imread(directory+str(n+1)+'-'+str(p)+'.png')
        intensity=np.append(intensity,np.average(pixel_intensity))

    return intensity

if __name__ == "__main__":

    #basic_calibrate()

    #gradient_calibrate()

    #polyfit_calibrate()

    #three_cross_section()

    #gradient_calibrate_new()

    #three_cross_section_new()

    gradient_calibrate_pixel()
