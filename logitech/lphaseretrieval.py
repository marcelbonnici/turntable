import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from tifffile import imsave
import os, os.path

def phaseshift(directory):
    """
    With an N-step fringe projection performed prior, outputting N number of
    webcam images in a directory, this function makes a phase shift map
    accordingly.
    """
    Iarr=np.array([])

    length=Image.open(directory+'/1.png').size[0] # gets length of exemplary webcam picture
    height=Image.open(directory+'/1.png').size[1] # gets height of exemplary webcam picture

    sin=np.zeros((height,length)) # prepares array to intake sin values
    cos=np.zeros((height,length)) # prepares array to intake cos values

    n=0
    N=len([name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))])
    for n in range (N): #for every step image in the directory
        I=Image.open(directory+'/'+str(n+1)+'.png') # images are titled from 1 to N
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

def graph(math, title):
    plt.rcParams.update({'font.size': 22})
    plt.imshow(math, cmap='gray', interpolation='none')
    cbar=plt.colorbar()
    plt.title(title)
    plt.show()

def xyz(u, title):
    m,n=u.shape
    R,C=np.mgrid[:m,:n]
    expression=np.column_stack((C.ravel(),R.ravel(), u.ravel()))
    np.savetxt(title, expression[:,:], delimiter=" ")

def intensity_cross_sctn(map, index, titl):
    plt.rcParams.update({'font.size': 22})
    plt.plot(np.arange(960),map[int(index)])
    plt.title(titl)
    plt.show()

if __name__ == "__main__":

    low=phaseshift('wall_low')
    high=phaseshift('wall_high')
    unwrapped_0=unwrap(low, high, .5, 30)

    xyz((unwrapped_0-unwrapped_0)[155:440,385:-385]*-1, "wall.xyz")
    low=phaseshift('p45_low')
    high=phaseshift('p45_high')
    unwrapped=unwrap(low,high, .5, 30)
    u=(552/408)*(unwrapped-unwrapped_0)
    xyz(u[155:440,385:-385], "p45deg.xyz")

    low=phaseshift('lphaseimgs20_low')
    high=phaseshift('lphaseimgs20_high')
    unwrapped=unwrap(low,high, .5, 30)
    u=(552/408)*(unwrapped-unwrapped_0)

    intensity_cross_sctn(u, 1*u.shape[0]/4, 'Pixel Intensity @ 0 degrees, 1/4-Way Down')

    low=phaseshift('n30_low')
    high=phaseshift('n30_high')
    unwrapped=unwrap(low,high, .5, 30)
    u=(552/408)*(unwrapped-unwrapped_0)
    #graph(u, 'ndeg')
    xyz(u[155:440,385:-385], "n30deg.xyz")

    low=phaseshift('p30_low')
    high=phaseshift('p30_high')
    unwrapped=unwrap(low,high, .5, 30)
    u=(552/408)*(unwrapped-unwrapped_0)
    #graph(u, 'pdeg')
    xyz(u[155:440,385:-385], "p30deg.xyz")
