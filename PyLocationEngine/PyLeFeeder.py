import sys
import argparse
from datetime import datetime

import pandas

import DataAnalazyer as da

gFilename = ""
gOutput = ""
gIndex = -1

####################
# handle arguments passed to the script
def handle_main_arg():
    global gFilename
    global gOutput
    parser = argparse.ArgumentParser()
    parser.add_argument("-v","--verbose", help="enable verbosity mode ", action="store_true")
    parser.add_argument("-f","--file", required=True, help="File name to read the data from")
    parser.add_argument("-o","--output", required=True, help="File name to write the command (ex: /home/pi/dev/spi0chip0/stdin)")
    parser.add_argument("-i","--index", help="index of the data in the file to be used")
    args = parser.parse_args()
    if args.file:
        gFilename = args.file 
    if args.output:
        gOutput = args.output
    if args.index:
        gIndex = args.index

####################
def main():
    global gOutput
    global gIndex
    global gFilename

    #print ("Python version:"+sys.version)

    datas = da.DataAnalyzer(gFilename)
    XData = datas.getXs()
    #print(XData[0])

    #print(datas.getXinInt(0))
    #YData = datas.getYs()

    #print("gOutput:",gOutput)
    f = open(gOutput, "w")
    if(gIndex!=-1):
        line = datas.getSerializedX(gIndex)
    else:
        line = datas.getSerializedX(0)
    line = "feedle " + line + "\r"
    print(line)
    f.write(line)

    
       
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