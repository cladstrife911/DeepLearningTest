import os
import pandas
import csv
import numpy as np

class DataAnalyzer:
    _XCol = []
    _XData = []
    _YData = []
    _YCol = []
    _gOffsetvalue = 40
    _gOffsetActive = False
    _gNumberOfSample = 0
    _filename = ""
    _filetype =""
    _dataFrame = pandas.DataFrame()

    # TODO: make the list of d_x configurable
    def __init__(self, filename):
        self._filename = filename
        with open(self._filename, newline='') as file:
            line = file.readline()
            if(line.find("[UwbM] LE")):
                print("Log from stderr")
                self._filetype = "stderr"
            else:
                print("Log from python analysis")
                self._filetype = "analysis"

        if self._filetype == "analysis":
            self._dataFrame = pandas.read_csv(filename, delimiter='\t', skipinitialspace=True , header=0)
            self._XCol = self._dataFrame[['#d_01', '#d_03', '#d_04', '#d_06', '#d_07', '#d_08', '#d_18']]
            self._YCol = self._dataFrame[['#X True', '#Y True', '#Z True']]
            self._XData = self._XCol.values
            self._YData = self._YCol.values
            self.fn = filename
            self._gNumberOfSample = self._dataFrame.shape[0]
            #print("# of sample in file:", self._gNumberOfSample)
        elif self._filetype == "stderr":
            self._XCol = self.prepareDataFrame()
            self._XData = self._XCol.values
        else:
            print("Error on file format")


    def prepareDataFrame(self):
        with open(self._filename, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            #File sample:
            #79176 [UwbM] LE;644;591;155;169;195;318;392;3;3;1;5;6;-457;-79;-62;0;
            #79272 [UwbM] LE;644;591;155;169;195;318;392;3;3;1;5;6;-454;-80;-62;0;
            self.npArrayD1= np.empty(0)
            self.npArrayD3= np.empty(0)
            self.npArrayD4= np.empty(0)
            self.npArrayD6= np.empty(0)
            self.npArrayD7= np.empty(0)
            self.npArrayD8= np.empty(0)
            self.npArrayD18= np.empty(0)
            for row in reader:
                if(row[0].find("[UwbM] LE")):
                    if row[1] != "-100":
                        #for i in range(7):
                        self.npArrayD1 = np.append(self.npArrayD1, float(row[1])/100)
                        self.npArrayD3 = np.append(self.npArrayD3, float(row[2])/100)
                        self.npArrayD4 = np.append(self.npArrayD4, float(row[3])/100)
                        self.npArrayD6 = np.append(self.npArrayD6, float(row[4])/100)
                        self.npArrayD7 = np.append(self.npArrayD7, float(row[5])/100)
                        self.npArrayD8 = np.append(self.npArrayD8, float(row[6])/100)
                        self.npArrayD18 = np.append(self.npArrayD18, float(row[7])/100)
                        #print("D1:", float(row[1])/100, "D18:",float(row[7])/100)
                else:
                    print("Error on file format")
            #print(self.npArrayD1.size, self.npArrayD3.size,
            #      self.npArrayD4.size,self.npArrayD6.size,
            #      self.npArrayD7.size,self.npArrayD8.size,
            #      self.npArrayD18.size)
            self._gNumberOfSample = self.npArrayD1.size
            self._XCol = pandas.DataFrame({'#d_01':self.npArrayD1,'#d_03':self.npArrayD3, '#d_04': self.npArrayD4, '#d_6':self.npArrayD6, '#d_07': self.npArrayD7, '#d_08': self.npArrayD8, '#d_18':self.npArrayD18 })
        return self._XCol

    def getNumberOfSamples(self):
        #print("self._gNumberOfSample: ", self._gNumberOfSample)
        return self._gNumberOfSample

    # Get X values (used as input for deep learning)
    def getXs(self):
        return self._XData

    # Return one line of XData converted into string int*100
    def getSerializedX(self, index):
        #print("getSerializedX:", index)
        if(index<self._gNumberOfSample):
            self._XDataInt = self._XData[index] * 100
            #print("self._XDataInt*100:", self._XDataInt)
            self._XDataInt = self._XDataInt.round(0)
            st = str((self._XDataInt).tolist())
            st = ''.join(st.replace('.0','').replace(',','').replace('[','').replace(']',''))
            #print("self._XDataInt:", st)
        else:
            st ="0 0 0 0 0 0 0"
        return st

    #get Y values (output of neural network)
    def getYs(self):
        return self._YData

    #True to apply, False to remove
    def applyOffset(self, bVal):
        if(bVal==True) and (self._gOffsetActive==False):
            self._gOffsetActive = True
            self._YData = self._YData - self._gOffsetvalue
        elif (bVal==False) and (self._gOffsetActive==True):
            self._YData = self._YData + self._gOffsetvalue
            self._gOffsetActive = False
        else:
            pass
        return self._YData
