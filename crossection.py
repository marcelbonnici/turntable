"""
For calibration Plotting
"""
import numpy as np
import matplotlib.pyplot as plt
import cv2
import csv
"""
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
"""
"""
p51=cv2.imread('pitchblacktest1.png')
#p102=cv2.imread('calib/102.png')
#p153=cv2.imread('calib/153.png')
#p204=cv2.imread('calib/204.png')
#p255=cv2.imread('calib/255.png')
plt.hist(p51.ravel(), color='red', bins = 40)
#plt.hist(p102.ravel(), color='orange', bins = 40)
#plt.hist(p153.ravel(), color='green', bins = 40)
#plt.hist(p204.ravel(), color='blue', bins = 40)
#plt.hist(p255.ravel(), color='purple', bins = 40)
axes = plt.gca()
axes.set_xlim([0,255])
axes.set_ylim([0,50])
plt.xlabel('Grayscale Value')
plt.ylabel('Frequency')
plt.title('Histogram of Input Image')
plt.show()
"""
"""
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
"""
"""
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
"""
"""
pic=cv2.imread('pitchblacktest1.png')
#pic1=cv2.imread('pitchblacktest1.png')
picdraw=cv2.imread('pitchblacktest.png')
for i in range (pic.shape[0]):
    for j in range (pic.shape[1]):
        if pic[i][j][0]!=0 or pic[i][j][1]!=0 or pic[i][j][2]!=0:
            print(pic[i][j])
            picdraw = cv2.rectangle(picdraw, (j-2,i-2), (j+2,i+2), (255,0,0), 1)
cv2.imshow('hi', picdraw)
cv2.imwrite('pitchblackblue1.png',picdraw)

cv2.waitKey(0) # waits until a key is pressed
cv2.destroyAllWindows() # destroys the window showing image
"""

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
