# Automated Photographic Turntable for 3D Modeling
---
This open source project combines mechatronics and computer vision to find the depth of objects at every angle. The hardware is accomplished with an Arduino microcontroller powering a sturdy LEGO® turntable, which is controlled by a made-from-scratch python module rotating an object to observe all its geometry.

## Motivation
---
As a mechatronics enthusiast, computer vision is a necessary skill to hone. When advised to make this project open source, it was logical to build the turntable from cherished LEGO® bricks to make it affordable, too.

## Video Demonstration
---
[![Turntable Fringe Projection](README-images/low_phase_map.png)](https://youtu.be/qwdusc)

## Hardware
---
* [Arduino UNO](https://store.arduino.cc/usa/arduino-uno-rev3)
* [Stepper Motor Driver Module](https://amzn.to/37S7ufj)
* [NEMA17 Stepper Motor](https://amzn.to/2M3aJK2)
* [Breadboard](https://www.amazon.com/DEYUE-breadboard-Set-Prototype-Board/dp/B07LFD4LT6/ref=sr_1_4?dchild=1&keywords=solderless+breadboard&qid=1598765073&sr=8-4)
* [USB Data Sync Cable](https://www.amazon.com/Data-Sync-Cable-Arduino-Microcontroller/dp/B01N9IP8LF/ref=sr_1_1?dchild=1&keywords=arduino+usb+cable&qid=1584604166&sr=8-1)
* 100µF Capacitor
* Jumper Wires
* Webcam or Digital Camera, capable of manual exposure and with female threaded receptacle

The LEGO® brick parts can be acquired by download the [CAD file](turntable_parts.lxf), and following [this tutorial](https://youtu.be/Y3sZaeOtZ2o?t=13) to purchase them. Access building instructions by downloading [LEGO Digital Designer](https://www.lego.com/en-us/ldd), opening the software and then clicking "Building Guide Mode" in the upper right corner. The bearings, which are white 1 x 1 round tiles in the file but transparent yellow in the below image, are to be placed in the slot of the large circle gear rack. The 4 decoupled L-beams are to be attached to the exposed friction pins exposed on the lower half of the bearing. The 2 x 3 plates, camera stand and projector stand are to be attached to the long beam coming from the turntable ground as one's triangulation circumstances require.

The Arduino electronic schematic can be followed below:
![Schematic](README-images/schem.png)

## Getting Started
---
### Requirements
The code files require:
1. [Arduino IDE](https://www.arduino.cc/en/main/software)
2. [Python 3](https://www.python.org/downloads/)
3. [Numpy](https://scipy.org/install.html)
4. [OpenCV](https://opencv.org/releases/)
5. [Serial](https://pypi.python.org/pypi/pyserial)
6. [Matplotlib](https://matplotlib.org/users/installing.html)
7. [The Python Standard Library (for time, subprocess, csv, threading, os, shutil)](https://docs.python.org/3/library/)

Before trying the required software and libraries, run the following from terminal:
`$ sudo apt update`

`$ sudo apt upgrade`
#### 1) Arduino IDE
`$ sudo apt install arduino`
#### 2) Python
`$ sudo apt install python3.6`
#### 3) Numpy
`$ sudo apt install python-numpy`
#### 4) OpenCV
`$ pip install opencv-python`
#### 5) Serial
`$ python -m pip install pyserial`
#### 6) Matplotlib
`$ python -m pip install -U matplotlib`

## Setting Up the Code
---
### Arduino UNO
Run `$ arduino` from terminal to open the IDE. Next, click `File > Open` and select `homework.ino`, located in the turntable folder in this repository.

Connect the microcontroller to the computer via the data sync cable. From the upper toolbar, click `Tools > Board > Arduino UNO` followed by `Tools > Serial Port` where the available port can be selected. In cases where more than one port is proposed, consult [this](https://www.mathworks.com/help/supportpkg/arduinoio/ug/find-arduino-port-on-windows-mac-and-linux.html) document from MathWorks.

Upload your code by clicking the rightwards arrow. Now onto the Python code!
### Python
