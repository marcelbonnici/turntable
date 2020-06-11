import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from tifffile import imsave

I0=Image.open('phaseimgs/1.png')
I1=Image.open('phaseimgs/2.png')
I2=Image.open('phaseimgs/3.png')
I3=Image.open('phaseimgs/4.png')

I0=np.asarray(I0, dtype='float32')
I1=np.asarray(I1, dtype='float32')
I2=np.asarray(I2, dtype='float32')
I3=np.asarray(I3, dtype='float32')

"""
I=np.array([I0,I1,I2,I3]).T
print(I.shape)
phase = np.arctan2(I[:,:,0] - I[:,:,2], I[:,:,1] - I[:,:,3])
"""

I=np.array([I0,I1,I2,I3])
print(I.shape)
phase = np.arctan2(I[0,:,:] - I[2,:,:], I[1,:,:] - I[3,:,:])

imsave('retrieval.tiff', phase)

plt.imshow(phase)

cbar=plt.colorbar()

plt.show()
