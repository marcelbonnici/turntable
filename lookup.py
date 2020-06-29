"""
Pinpoints projection value for desired capture value
"""
import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
#automate crossection > plot

def open_csv():
    results = []
    with open("fitplot.csv") as csvfile:
        reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC) # change contents to floats
        for row in reader: # each row is a list
            results.append(row)
    return np.asarray(results)

def lookup(table, desired_captured_intensity):#try dci for odd range, evenrange, and none

    desired_captured_intensity=int(desired_captured_intensity)
    if desired_captured_intensity<=table[-1][1]:
        x = np.where(table[:,1] == desired_captured_intensity)
        y = np.where(table[:,1] == 256)

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
        projected_loc=table[captured_loc][0]

    else:
        projected_loc=table[-1][0]

    return int(projected_loc)

def user_input():
    desired_captured_intensity=input("Desired Capture Intensity: ")
    projected_loc=lookup(table, int(desired_captured_intensity))
    print("Corresponding Projected Intensity: " + str(projected_loc))

def photo_input(n_steps):
    loca=0
    for shift in range (n_steps):
        loca=loca+1
        img = mpimg.imread('phasefringe/'+str(loca)+'.png')
        for i in range(img.shape[0]):
            for j in range (img.shape[1]):
                desired_captured_intensity=img[i,j,0]
                projected_loc=lookup(table, np.around(255*desired_captured_intensity))
                img[i,j]=np.asarray([projected_loc/255,projected_loc/255,projected_loc/255,1])
        plt.imsave('phasefringe/'+str(loca)+'edit.png',img,cmap='gray')
if __name__ == "__main__":
    table=open_csv()
    #user_input()
    photo_input(1)
