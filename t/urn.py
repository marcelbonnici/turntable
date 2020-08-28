import serial.tools.list_ports
import serial
import time
import tkinter as tk

"""
Find computer available ports for Arduino connectivity
"""
def get_ports():

    ports = serial.tools.list_ports.comports()
    return ports
"""
Select the port that is the Arduino's
"""
def findArduino(portsFound):

    commPort = 'None'
    numConnection = len(portsFound)

    for i in range(0,numConnection):
        port = foundPorts[i]
        strPort = str(port)
        if 'dev' in strPort or 'COM' in strPort: #If foudn on Linux or Windows
            splitPort = strPort.split(' ')
            commPort = (splitPort[0])

    return commPort

foundPorts = get_ports()
connectPort = findArduino(foundPorts)

if connectPort != 'None':
    arduinoData = serial.Serial(connectPort, 9600, timeout=5)
time.sleep(1)

"""
Input degrees truncated to the 3200th of a revolution
"""
def degrees(deg):
    try:
        go=int(51.8518518519*float(deg))
        arduinoData.write((str(go)+'\n').encode())
    except ValueError:
        print('Non-integer characters not allowed')

"""
Input degrees truncated to the 3200th of a revolution
"""
def fraction(frac):
    try:
        divider=float(frac)
        go=int(int(360.0/divider)/.01928571428)
        arduinoData.write((str(go)+'\n').encode())
    except ValueError:
        print('Non-integer characters not allowed')

def pjog():
    arduinoData.write(('89'+'\n').encode())
def njog():
    arduinoData.write(('-89'+'\n').encode())

def gui():
    def njog_gui():
         go=int(float(-10)/.01928571428)
         arduinoData.write((str(go)+'\n').encode())
    def pjog_gui():
         go=int(float(10)/.01928571428)
         arduinoData.write((str(go)+'\n').encode())
    def deg():
        try:
            go=int(float(number.get())/.01928571428) # The divisor is the conversion ratio from steps to turntable rotations
            arduinoData.write((str(go)+'\n').encode())
        except ValueError:
            print('Non-integer characters not allowed')
    def div():
        try:
            divider=float(number1.get())
            go=int(int(360.0/divider)/.01928571428)
            arduinoData.write((str(go)+'\n').encode())
        except ValueError:
            print('Non-integer characters not allowed')

    window=tk.Tk()
    Button=tk.Button
    Label=tk.Label

    #Source: https://codeloop.org/how-to-create-textbox-in-python-tkinter/
    number = tk.StringVar()
    degrees = Label(window, text="DEGREES")
    degfill = tk.Entry(window, width = 4, textvariable = number)
    submit = Button(window, text = "Submit", command = deg)

    number1 = tk.StringVar()
    divisions = Label(window, text="DIVISIONS")
    divfill = tk.Entry(window, width = 4, textvariable = number1)
    submit1 = Button(window, text = "Submit", command = div)

    jog  = Label(window, text="JOG")
    njog_btn = Button(window, text="-10 deg", command=njog_gui)
    pjog_btn = Button(window, text="+10 deg", command=pjog_gui)

    degrees.grid(row=0, column=1)
    degfill.grid(row=1, column=1)
    submit.grid(row=2, column=1)

    divisions.grid(row=3, column=1)
    divfill.grid(row=4, column=1)
    submit1.grid(row=5, column=1)

    jog.grid(row=6, column=1)
    pjog_btn.grid(row=7, column=1)
    njog_btn.grid(row=8, column=1)

    input('Press ENTER to close')
    window.mainloop()
