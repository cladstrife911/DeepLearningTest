import sys
import argparse
from datetime import datetime
import os
import random
import time

import pandas

import DataAnalazyer as da

gFilename = ""
gOutput = ""
gIndex = -1
gNumber = 0
gRandom = False
gDelay = 10

####################
# handle arguments passed to the script
def handle_main_arg():
    global gFilename
    global gOutput
    global gNumber
    global gRandom
    global gDelay
    parser = argparse.ArgumentParser()
    parser.add_argument("-v","--verbose", help="enable verbosity mode ", action="store_true")
    parser.add_argument("-f","--file", required=True, help="File name to read the data from")
    parser.add_argument("-o","--output", required=True, help="File name to write the command (ex: /home/pi/dev/spi0chip0/stdin)")
    parser.add_argument("-i","--index", help="index of the data in the file to be used")
    parser.add_argument("-n","--number", type=int, help="number of sample to play")
    parser.add_argument("-r","--random", help="play in random order", action="store_true")
    parser.add_argument("-d","--delay", type=int, help="delay in ms between writing")
    args = parser.parse_args()
    if args.file:
        gFilename = args.file 
    if args.output:
        gOutput = args.output
    if args.index:
        gIndex = args.index
    if args.number:
        gNumber = args.number
    if args.random:
        gRandom = True
    if args.delay:
        gDelay = args.delay

####################
def main():
    global gOutput
    global gIndex
    global gFilename
    global gRandom
    global gNumber
    global gDelay

    #print ("Python version:"+sys.version)

    datas = da.DataAnalyzer(gFilename)
    XData = datas.getXs()
    #print(XData[0])

    #print(datas.getXinInt(0))
    #YData = datas.getYs()

    #Open the file to be written
    fd = os.open(gOutput, os.O_WRONLY)
    #print("gOutput:",gOutput)
    print("gNumber:",gNumber)

    for c in range(gNumber):
        if(gRandom):
            gIndex = random.randint(0,datas.getNumberOfSamples())
        else:
            gIndex = c % datas.getNumberOfSamples()
        line = datas.getSerializedX(gIndex)
        line = "feedle " + line + "\r"
        print(line)
        os.write(fd, bytes(line,'UTF-8'))
        #convert wait time in ms
        time.sleep(gDelay/1000)

    #Finaly close the file
    os.close(fd)

    
       
    #print(YData[1])

    ### Test applyOffset function
    #print("Apply Offset:")
    #print(datas.applyOffset(True))
    #print("UnApply Offset:")
    #print(datas.applyOffset(False))
    #print("UnApply twice Offset (do nothing):")
    #print(datas.applyOffset(False))

####################
if __name__ == "__main__":
    handle_main_arg()
    main()
