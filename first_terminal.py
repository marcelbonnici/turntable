#! /usr/bin/env python
import argparse
import serial.tools.list_ports
import serial
import time
def run(args):
    foundPorts = serial.tools.list_ports.comports()

    commPort = 'None'
    numConnection = len(foundPorts)

    for i in range(0,numConnection):
        port = foundPorts[i]
        strPort = str(port)
        if 'dev' in strPort:
            splitPort = strPort.split(' ')
            commPort = (splitPort[0])
            connectPort=commPort
    if connectPort != 'None':
        arduinoData = serial.Serial(connectPort, 9600, timeout=5)
    time.sleep(1)



    if args.deg!=0:
        try:
            go=int(16*int(args.deg)/1.8)
            arduinoData.write((str(go)+'\n').encode())
        except ValueError:
            print('Non-integer characters not allowed')



    elif args.frac!=0:
        try:
            divider=int(args.frac)
            go=int(16*int(360/divider)/1.8)
            arduinoData.write((str(go)+'\n').encode())
        except ValueError:
            print('Non-integer characters not allowed')

    elif args.jog=='a':
        arduinoData.write(('-800'+'\n').encode())
    elif args.jog=='s':
        arduinoData.write(('-400'+'\n').encode())
    elif args.jog=='d':
        arduinoData.write(('-80'+'\n').encode())
    elif args.jog=='f':
        arduinoData.write(('80'+'\n').encode())
    elif args.jog=='g':
        arduinoData.write(('400'+'\n').encode())
    elif args.jog=='h':
        arduinoData.write(('800'+'\n').encode())

def main():
	parser=argparse.ArgumentParser(description="Convert a fastA file to a FastQ file")
	parser.add_argument("-deg",help="jog in degrees",dest="deg",type=str, default=0)
	parser.add_argument("-frac",help="fastq output filename" ,dest="frac", type=str, default=0)
	parser.add_argument("-jog",help="Quality score to fill in (since fasta doesn't have quality scores but fastq needs them. Default=I" ,dest="jog", type=str, default='z')
	parser.set_defaults(func=run)
	args=parser.parse_args()
	args.func(args)

if __name__=="__main__":
	main()
