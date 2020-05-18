import numpy as np
import matplotlib.pyplot as plt
import cv2
import time
import screeninfo
screencount=0
for m in screeninfo.get_monitors():
    width = int(m.width)
    height = int(m.height)
nu0=float(input('Enter X coefficient: '))
xi0=float(input('Enter Y coefficient: '))
color=int(input('Grayscale(0) or Default(1): '))
#MOVE
if color==1:
    cmap='color'
if color==0:
    color=255
    cmap='gray'
x=np.linspace(0,1,width)
y=np.linspace(0,1,height)
X,Y=np.meshgrid(x,y)

for shift in range(4):
    shift=shift*np.pi/2
    if cmap=='gray':
        img=(np.cos(nu0*X+xi0*Y+shift)/2+0.5)*color
        plt.imsave('fringe.jpg',img, cmap=cmap)
    else:
        img=np.cos(nu0*X+xi0*Y+shift)
        plt.imsave('fringe.jpg',img)

    image = cv2.imread('/home/marcelbonnici/Dropbox/000_LINUX/turntable/fringe.jpg')
    cv2.namedWindow("fringe", cv2.WND_PROP_FULLSCREEN)
    cv2.moveWindow('fringe',int(m.width),0)
    cv2.setWindowProperty("fringe",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

    cv2.imshow('fringe', image)

    key = cv2.waitKey(250)

    if key == 27:#if ESC is pressed, exit loop
        cv2.destroyAllWindows()
        break
