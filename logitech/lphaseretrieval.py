import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from tifffile import imsave
import os, os.path
import cv2

def phaseshift(directory):
    Iarr=np.array([])

    length=Image.open(directory+'/1.png').size[0]
    height=Image.open(directory+'/1.png').size[1]

    sin=np.zeros((height,length))
    cos=np.zeros((height,length))
    #sin=np.zeros((2448,3264))
    #cos=np.zeros((2448,3264))
    n=0
    N=len([name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))])
    for n in range (N):
        I=Image.open(directory+'/'+str(n+1)+'.png')
        I=np.asarray(I, dtype='float32')
        sin=sin+I*np.sin(2*np.pi*n/N)
        cos=cos+I*np.cos(2*np.pi*n/N)
    phase = np.arctan2(cos,sin) #cos, sin wrt simpler paper

    return phase

def unwrap(low, high):
    un=high+(2*np.pi)*np.around((60*low-high)/(2*np.pi)) # 60 cuz 30/.5
    return un

def depthmap(u):
    u=(u-np.min(u))/(np.max(u)-np.min(u)) #2448 CHANGED

    #u=masked_phase_no_noise(u)

    xyz(u)
    return u

def graph(math):
    plt.rcParams.update({'font.size': 22})
    plt.imshow(math, cmap='gray', interpolation='none')
    cbar=plt.colorbar()
    #mn=np.floor(math.min())
    #mx=np.ceil(math.max())
    #md=(mx-mn)/2
    #cbar.set_ticks([-.05,0,.05])
    #cbar.set_ticklabels([-.05,0,.05])
    plt.title("Unwrapped Phase Map")
    plt.show()

def intensity_modulation(directory):

    N=len([name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))])
    total=np.array([])

    for n in range (N):
        I=Image.open(directory+'/'+str(n+1)+'.png')
        I=np.asarray(I, dtype='float32')

        if total.shape[0]==0:
            total=I
        else:
            total=total+I

    total=total/N
    total=total.astype(int)
    total=np.abs(total-255)

    plt.imshow(total, cmap="Greys")
    plt.imsave('6pics/average_intensity.png', total, cmap='Greys')
    plt.show()

def average_intensity (directory):

    N=len([name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))])
    total=np.array([])

    for i in range (51,256):
        for j in range (5):

            I=Image.open(directory+'/'+str(i)+'-'+str(j)+'.png')
            I=np.asarray(I, dtype='float32')

            if total.shape[0]==0:
                total=I
            else:
                total=total+I

    total=total/N
    total=total.astype(int)
    total=np.abs(total-255)

    plt.imshow(total, cmap="Greys")
    plt.imsave('6pics/intensity_modulation.png', total, cmap='Greys')
    plt.show()

def binarized_intensity_modulation(threshold):
    I=np.array(Image.open('6pics/intensity_modulation.png'))

    I = np.where(I > threshold, 0, 255)
    I=I[:,:,0]
    plt.imshow(I, cmap="Greys")
    plt.imsave('6pics/binarized_intensity_modulation.png', I, cmap='Greys')
    plt.show()

def masked_phase_no_noise(u):
    return np.where(u > (.5)*2448, u, 0)

def masked_phase_f(unwrapped, unwrapped_0):
    z=(unwrapped-unwrapped_0)[155:-155,280:-210]
    min=np.min(z)
    max=np.max(z)
    bin=np.array(Image.open('6pics/binarized_intensity_modulation.png'))[155:-155,280:-210,0]
    z=np.where(bin==0, 9999, z)
    z=np.where(z==9999, np.min(z), z)
    return z

def xyz(u):
    m,n=u.shape
    R,C=np.mgrid[:m,:n]
    expression=np.column_stack((C.ravel(),R.ravel(), u.ravel()))
    np.savetxt("output.xyz", expression[:,:], delimiter=" ")

if __name__ == "__main__":

    low=phaseshift('steppics/s0')
    high=phaseshift('steppics/l0')
    unwrapped_0=unwrap(low,high)

    low=phaseshift('steppics/sloop')
    high=phaseshift('steppics/lloop')
    unwrapped=unwrap(low,high)

    z=((504/64)*(unwrapped-unwrapped_0))[155:-155,280:-210]

    u=depthmap(z)

    #average_intensity('lampcalibgradient') # Part B, Graphing Included
    # unwrapped() is Part C, Graphing Excluded
    #intensity_modulation('steppics/llamp') #Part D, Graphing Included
    #binarized_intensity_modulation(210) # Part E, Graphing Included
    #z=masked_phase_f(unwrapped, unwrapped_0) #Part F, Graphing Excluded
    #graph(z)
