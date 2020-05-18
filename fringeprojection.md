# Fringe Projection 101
* The recognition that patterned illumination may be used to simultaneously super resolve and recover topography information is a key contribution to patterned illumination

## Mechanics of Phase Measurement Profilometry
* Phase Measurement Profilometry (PMP) is a measurement technique that recovers densely sampled topographic information from images of a scene illuminated by one or more periodic sinusoidal patterns.


* The expression for the detected intensity under the periodic illumination
#### Periodic Illumination
![](https://lh3.googleusercontent.com/5miPTtWmokxwEc11HZ_5utigHPJyCW7L6B7BrMBNaQXsONZI_HDQ__AIQjL2zWgIYcwxrCzgJG_sqlWQLdjvPsE_cwpkeQ5hy3Oz97ZgO37Pc0vUwk-N0oTj3wZXUoH_H_uPtfxd) ...lends itself to...
#### Detected intensity
![](https://lh6.googleusercontent.com/wkGM17ckYzOYsQewkudxQjq6CtesIV2JnWiyNQ8EsX-A_TMNW7kEAcss8evv47aLcgtqZk1E_62YpeVjugVA-1roGZnAF70wKhCw3bR3ZWcFpZPLZnrcyAGzI_6Cl8DdSlo__p3w)
![](https://lh4.googleusercontent.com/JULF3gwiQ-wRAydRl3GU7fc8-7P4gHPq_ewMwxAk5oC37uKGsp9iQtL-UrYWzzSNVC4lVYQ58OgvF1WhOYoyj8vYmuBMDaYWZrmX2dm2bctzj2tBq2y_laSIt8FlLiby7CXOAOv5)


* In PMP, it is common practice to ignore the effect of blurring due to the imaging optics. This practice is admissible when one of two conditions is satisfied:
1. The primary objective is to identify qualitative(not quantitative) topographic information.
2. The support of the camera PSF is tighter than the physical size of a camera pixel.

The present work restricts its attention to qualitative topographic information, so that the reference to
the camera PSFcam may be dropped from the detected intensity equation. In addition, the phase arg(B(u, v)) may be set to zero under the assumption that the illumination optics is diffraction limited.

Incorporating these constraints into the equation yields the following
![](https://lh4.googleusercontent.com/LS3GkuN0NfslFcUtvv5EmMyW-Y9azc4o9ySHUQ7_PTgT98AJk7hsWXWJfBdx6WyunSQ1rFXRCpxnI0vP2LW9KU9aGFPGJ_bg88bVxZOC)

#### Scene Recovery using Phase Measurement Profilometry

The standard approach to recovering topographic information in PMP
![](https://lh4.googleusercontent.com/4Q61d6Xiw5XvHRJShoS5drCTzAkGiRn09VOWEnJmZ4l2wQL9oXOAeTnE86u94ynaV8n8WLQV2yFMNF7UN2JEKF-U8a8r2lQhZ4TTmNKLLOWz0I29vh0ZfxjEclhqbBUI9h8m60m5)

The wrapped equation holds the four phases of a period, each shifted by 90 degrees. The last equation is the last equation of the last section, rewritten in terms of W.

#### Phase Unwrapping in Phase Measurement Profilometry
Below is an elegant solution to phase unwrapping
![](https://lh4.googleusercontent.com/8TBCKzYKcnO6kSM1bkVzNuxgkacdjlUrE0x7GDdXav3VTSjrmBSNfAb_5uFRup0vbdrdIoPh7IwuRIQ7D6GweFyucvS0dP6aSvoUVgoc6Ccj_ixKWjjzxeIpsVyMMsJsDXcO4UdU)
* The grayscale phase map, which is this project's map of choice, is free of artifacts, which does not require unwrapping, which the high distortion phase map does.

This scene recovery technique does not impose constraints on the position/orientation of the camera and projector.

The undeniable allure of super resolving spatial detail while recovering topographic information, encourages us to restrict our attention to stereo arrangements that support super resolution. A list of these stereo arrangements is enumerated below:
![](https://lh6.googleusercontent.com/7qnQs_JH08w0r2rDzDwMjKk4FzGGUzP1psMuIXjw6vkXG0i8rlf8o2t3F0aTk7e9kcIo4XTwzf5mfqVrnwqk6lSGgBI9D8Y34S4XFvtwCOTXLgyDTxFjMd50UAs6imJ622340D3e)
![](https://lh3.googleusercontent.com/4qhzxkNTDjFELk0-9qJ-YesUqXkaMZe6RQuYxug1jyJTZWxWXgF4sN3fpgATMNEbkSyNdxZcuQ7IKehq9Wv2zObrPd4756ec5QayBKqxQoWE_7MYNaglYdecI6MqU_MhpP_h_i7K)
![](https://lh4.googleusercontent.com/QyhlrA9ycm315H4RUtj4mHuy6_3aNAknNIWo-MC0AVbW4a2sPunAz5TfVXr6wivh8VWFACVCWN9w6iq2s2AZGsUpkuLneRI3j9aU4RRecMyDGkj_fLsNDfiNBq3-GmmDklgleEeF)

###### Why does bz=0?

Imaging and illumination systems are almost always mounted on a single arm and possibly
collocated. The above finding has valuable practical implications in that it hints at the possibility of using
Structured Light Scanners to super resolve spatial detail in addition to recovering topographic information.

#### Scene recovery in a canonical stereo setup using periodic sinusoidal
![](https://lh3.googleusercontent.com/mPwHbW5R8jSFufkcmLmWWdojkCP6GVPy-Z6HLN3HSpx1A4ssTsyBvcwD5tdFJeFIA2JQczZeaoCiZ4S1cPMAn4fDhfZpn2dZRlNUvPuRhZ8Qb0EkynNeCPeRDs0THKDIunVSxI9V)
![](https://lh4.googleusercontent.com/-eoZh1Qv7a43Fk6iyRLIoUNrlRERoaTl-Fg9eCyJAmedaDdg0QkrX9-mFr42oz2-NMeUMjA60MQ9VcLbZLiKSL9cxSJRLXlHnki_bZI-46SXs837CrBnwnKZpF6wQK1yVLLzdLCr)

#### Range Resolution
![](https://lh6.googleusercontent.com/TREQRt1tRQoIZZ1JrHyyXNx5lVof8Et_SR5stAb5LWKKze0Ny6L35MQlOwfMYB_t9ntJ_FOUVaca2jEFhkZK0tv6geJmshoWrhusmWHXyOEbe41QNX6tvvWo2GtnH0222n4eeqTs)
![](https://lh5.googleusercontent.com/8tOANWi8abIvMFr1isEZI7g2qsZQnPF38MIV64H5MUbGEgRHufMNEO9cnLLU4UX1ZM2qJpmy45RN9e1v3cGItiLId9_6IcSGTb74DqP3wOSInZZT_K9aLTmWXnGClTVPYkXiHLAk)

#### Final Points
Below demonstrates the potential benefit of projecting warped sinusoidal patterns in a collocated stereo arrangement. Panel-1 illustrates the camera image under periodic sinusoidal illumination. Panel-2 illustrates the camera image under warped sinusoidal illumination.
![](https://lh4.googleusercontent.com/hCqktHzMhl3Uxtih2CQYWnDN2qAo1y6hg-f-0lcgfwFKQ52snIrEtsmfyIZrO0KTZHwPekxkqnU-W7V5xaxeUKEtisPa5NhfEtg5HreCJgbn0kv_ZIXmgUXX7mRvruMTNzR9aBTQ)

Panel-2 uses a method that keeps the stripes from blending.

## SUMMARY
Our inquiry into the mechanics of scene recovery concludes with the following key observations:
1. Active scene recovery is predicated on the observation of parallax induced phase distortion in the
camera image acquired under sinusoidal illumination.
2. Any active stereo apparatus may be used to recover topographic information, from the camera images
acquired under sinusoidal or warped sinusoidal illumination.
94
3. A single collocated stereo apparatus (=) supports the joint recovery of topographic information
and spatial detail lost to the camera optical blur.
