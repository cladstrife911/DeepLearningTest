import sys
import argparse
import pandas
import csv
import numpy as np

gFilename=""
gOutput=""


class LogCleaner:
    def __init__(self, filename, Outputfilename, header="LEv1", limiter=";"):
        self._filename = filename
        self._Outputfilename = Outputfilename
        self._header = header
        self._limiter = limiter
        if Outputfilename=="":
            self._Outputfilename = self._filename.replace('.csv', '_cleaned.csv')


    def CleanUp(self):
        output = open(self._Outputfilename, "w")
        with open(self._filename, newline='') as file:
            line = file.readline()
            while line:
                line = line.replace('"', '')
                if self._header in line:
                    output.write(line)
                line = file.readline() #read next line


                ####################
# handle arguments passed to the script
def handle_main_arg():
    global gFilename
    global gOutput


    parser = argparse.ArgumentParser()
    parser.add_argument("-f","--file", required=True, help="File name to read the data from")
    parser.add_argument("-o","--output", help="File name to write the command (ex: /home/pi/dev/spi0chip0/stdin)")
    args = parser.parse_args()
    if args.file:
        gFilename = args.file
    if args.output:
        gOutput = args.output

####################
def main():
    global gFilename
    global gOutput
    print("Cleaning "+ gFilename + " into "+ gOutput +"...")
    lc = LogCleaner(gFilename, gOutput)
    lc.CleanUp()
    print("Cleaning Done")

####################
if __name__ == "__main__":
    handle_main_arg()
    main()