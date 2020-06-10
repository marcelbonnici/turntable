import numpy as np
import matplotlib.pyplot as plt
import cv2

I0=cv2.imread('phaseimgs/1.png')#shift by 0
I1=cv2.imread('phaseimgs/2.png')#shift by pi/2
I2=cv2.imread('phaseimgs/3.png')#shift by pi
I3=cv2.imread('phaseimgs/4.png')#shift by 3*pi/2

#np.atan does not exist, I assumed np.arctan was the substitute
phase = -1*np.arctan(I0-I2/I1-I3) #Multiplied by -1 to make values positive

phase *= 40.584510488 #2*pi * 40.584... = 255

cv2.imwrite('retrieval.jpg',np.nan_to_num(phase))
