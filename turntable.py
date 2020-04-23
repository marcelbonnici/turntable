import serial.tools.list_ports
import serial
import tkinter as tk
#from tkinter import ttk

def get_ports():

    ports = serial.tools.list_ports.comports()
    #print(ports)
    return ports

def findArduino(portsFound):

    commPort = 'None'
    numConnection = len(portsFound)

    for i in range(0,numConnection):
        port = foundPorts[i]
        strPort = str(port)
        if 'dev' in strPort:
            splitPort = strPort.split(' ')
            commPort = (splitPort[0])

    return commPort


foundPorts = get_ports()
connectPort = findArduino(foundPorts)

if connectPort != 'None':
    arduinoData = serial.Serial(connectPort, 9600, timeout=5)

def jog_neg_9():
    arduinoData.write(('-5'+'\n').encode())
def jog_neg_45():
    arduinoData.write(('-25'+'\n').encode())
def jog_neg_90():
    arduinoData.write(('-50'+'\n').encode())
def jog_pos_9():
    arduinoData.write(('5'+'\n').encode())
def jog_pos_45():
    arduinoData.write(('25'+'\n').encode())
def jog_pos_90():
    arduinoData.write(('50'+'\n').encode())
def deg():
    go=int(int(number.get())/1.8)
    arduinoData.write((str(go)+'\n').encode())
def div():
    divider=int(number1.get())
    go=int(int(360/divider)/1.8)
    arduinoData.write((str(go)+'\n').encode())
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
btn  = Button(window, text="-9 deg", command=jog_neg_9)
btn1 = Button(window, text="-45 deg", command=jog_neg_45)
btn2 = Button(window, text="-90 deg", command=jog_neg_90)
btn3 = Button(window, text="+9 deg", command=jog_pos_9)
btn4 = Button(window, text="+45 deg", command=jog_pos_45)
btn5 = Button(window, text="+90 deg", command=jog_pos_90)

degrees.grid(row=0, column=1)
degfill.grid(row=1, column=1)
submit.grid(row=2, column=1)
divisions.grid(row=3, column=1)
divfill.grid(row=4, column=1)
submit1.grid(row=5, column=1)
jog.grid(row=6, column=1)
btn3.grid(row=7, column=0)
btn4.grid(row=7, column=1)
btn5.grid(row=7, column=2)
btn.grid(row=8, column=0)
btn1.grid(row=8, column=1)
btn2.grid(row=8, column=2)

input("Press ENTER to close")
window.mainloop()
arduinoData.close()
