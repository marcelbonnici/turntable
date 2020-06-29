import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from tifffile import imsave
import os, os.path

def phaseshift(directory):
    Iarr=np.array([])
    sin=np.zeros((2448,3264))
    cos=np.zeros((2448,3264))
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
    un=high+(2*np.pi)*np.around((40*low-high)/(2*np.pi))
    return un

def depthmap(u):
    u=(u-np.min(u))*2448/(np.max(u)-np.min(u))
    m,n=u.shape
    R,C=np.mgrid[:m,:n]
    expression=np.column_stack((C.ravel(),R.ravel(), u.ravel()))
    np.savetxt("output.xyz", expression[:,:], delimiter=" ")
    return u

def graph(math):
    plt.imshow(math)
    cbar=plt.colorbar()
    #mn=np.floor(math.min())
    #mx=np.ceil(math.max())
    #md=(mx-mn)/2
    #cbar.set_ticks([-.05,0,.05])
    #cbar.set_ticklabels([-.05,0,.05])
    plt.title("Qualitative Depth Map")
    plt.show()

if __name__ == "__main__":
    low=phaseshift('phaseimgs')
    high=phaseshift('phaseimgs40')
    unwrapped=unwrap(low,high)
    depth=depthmap(unwrapped)

    #test=depth
    #test=np.nan_to_num(np.power(unwrapped,-1),posinf=0,neginf=0)
    #test[test<-.05]=0
    #test[test>.05]=0
    graph(depth)
    print(np.max(depth))
    print(np.min(depth))
    print(np.median(depth))
