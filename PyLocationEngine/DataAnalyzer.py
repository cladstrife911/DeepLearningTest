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
    # _dataFrame = pandas.DataFrame()

    # TODO: make the list of d_x configurable
    def __init__(self, filename):
        self._filename = filename
        with open(self._filename, newline='') as file:
            # self._filetype = "stderr"
            if '[UwbM] LEv1' in file.read():
                print("Log from stderr")
                self._filetype = "stderrLEv1"
            elif '[UwbM] LE' in file.read():
                print("Log from stderr")
                self._filetype = "stderr"
            else:
                print("Log from python analysis")
                self._filetype = "analysis"

        if self._filetype == "analysis":
            # self._dataFrame = pandas.read_csv(filename, delimiter='\t', skipinitialspace=True , header=0)
            # self._XCol = self._dataFrame[['#d_01', '#d_03', '#d_04', '#d_06', '#d_07', '#d_08', '#d_18']]
            # self._YCol = self._dataFrame[['#X True', '#Y True', '#Z True']]
            # self._XData = self._XCol.values
            # self._YData = self._YCol.values
            # self.fn = filename
            self._gNumberOfSample = 10
            print("# of sample in file:", self._gNumberOfSample)
        elif self._filetype == "stderr":
            self._XCol = self.prepareDataFrame()
            self._XData = self._XCol.values
        elif self._filetype == "stderrLEv1":
            self._XCol = self.prepareDataFrameLEv1()
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

    def prepareDataFrameLEv1(self):
        with open(self._filename, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            #File sample:
            #742869	[UwbM] LEv1	986	-104 -77 607 -103 -88 174 -53 -52 201 -72 -66 217 -89 -72 259 -73 -70 356 -79 -74 3 4800
            self.npArrayD1= np.empty(0)
            self.npArrayP1= np.empty(0)
            self.npArrayD3= np.empty(0)
            self.npArrayP3= np.empty(0)
            self.npArrayD4= np.empty(0)
            self.npArrayP4= np.empty(0)
            self.npArrayD6= np.empty(0)
            self.npArrayP6= np.empty(0)
            self.npArrayD7= np.empty(0)
            self.npArrayP7= np.empty(0)
            self.npArrayD8= np.empty(0)
            self.npArrayP8= np.empty(0)
            self.npArrayD14= np.empty(0)
            self.npArrayP14= np.empty(0)
            for row in reader:
                if(row[1] == '[UwbM] LEv1'):
                    # if row[1] != "-100":
                    # for i in range(7):
                    row_num = 2
                    if row[row_num]=="nan" or row[row_num]=="-100":
                        self.npArrayD1 = np.append(self.npArrayD1, 1000)
                        self.npArrayP1 = np.append(self.npArrayP1, -109)
                    else:
                        self.npArrayD1 = np.append(self.npArrayD1, float(row[row_num]))
                        self.npArrayP1 = np.append(self.npArrayP1, float(row[row_num+1]))

                    row_num = 5
                    if row[row_num]=="nan" or row[row_num]=="-100":
                        self.npArrayD3 = np.append(self.npArrayD3, 1000)
                        self.npArrayP3 = np.append(self.npArrayP3, -109)
                    else:
                        self.npArrayD3 = np.append(self.npArrayD3, float(row[row_num]))
                        self.npArrayP3 = np.append(self.npArrayP3, float(row[row_num+1]))

                    row_num=8
                    if row[row_num]=="nan" or row[row_num]=="-100":
                        self.npArrayD4 = np.append(self.npArrayD4, 1000)
                        self.npArrayP4 = np.append(self.npArrayP4, -109)
                    else:
                        self.npArrayD4 = np.append(self.npArrayD4, float(row[row_num]))
                        self.npArrayP4 = np.append(self.npArrayP4, float(row[row_num+1]))

                    row_num=11
                    if row[row_num]=="nan" or row[row_num]=="-100":
                        self.npArrayD6 = np.append(self.npArrayD6, 1000)
                        self.npArrayP6 = np.append(self.npArrayP6, -109)
                    else:
                        self.npArrayD6 = np.append(self.npArrayD6, float(row[row_num]))
                        self.npArrayP6 = np.append(self.npArrayP6, float(row[row_num+1]))

                    row_num=14
                    if row[row_num]=="nan" or row[row_num]=="-100":
                        self.npArrayD7 = np.append(self.npArrayD7, 1000)
                        self.npArrayP7 = np.append(self.npArrayP7, -109)
                    else:
                        self.npArrayD7 = np.append(self.npArrayD7, float(row[row_num]))
                        self.npArrayP7 = np.append(self.npArrayP7, float(row[row_num+1]))

                    row_num=17
                    if row[row_num]=="nan" or row[row_num]=="-100":
                        self.npArrayD8 = np.append(self.npArrayD8, 1000)
                        self.npArrayP8 = np.append(self.npArrayP8, -109)
                    else:
                        self.npArrayD8 = np.append(self.npArrayD8, float(row[row_num]))
                        self.npArrayP8 = np.append(self.npArrayP8, float(row[row_num+1]))

                    row_num=20
                    if row[row_num]=="nan" or row[row_num]=="-100":
                        self.npArrayD14 = np.append(self.npArrayD14, 1000)
                        self.npArrayP14 = np.append(self.npArrayP14, -109)
                    else:
                        self.npArrayD14 = np.append(self.npArrayD14, float(row[row_num]))
                        self.npArrayP14 = np.append(self.npArrayP14, float(row[row_num+1]))

                else:
                    print("Error on file format")
                    #print(self.npArrayD1.size, self.npArrayD3.size,
                    #      self.npArrayD4.size,self.npArrayD6.size,
                    #      self.npArrayD7.size,self.npArrayD8.size,
                    #      self.npArrayD18.size)
                    self._gNumberOfSample = self.npArrayD1.size
                    self._XCol = pandas.DataFrame({'#d_01':self.npArrayD1,'#p_01':self.npArrayP1,
                                                   '#d_03':self.npArrayD3,'#p_03':self.npArrayP3,
                                                   '#d_04': self.npArrayD4, '#p_04': self.npArrayP4,
                                                   '#d_06':self.npArrayD6,'#p_06':self.npArrayP6,
                                                   '#d_07': self.npArrayD7,'#p_07': self.npArrayP7,
                                                   '#d_08': self.npArrayD8, '#p_08': self.npArrayP8,
                                                   '#d_14':self.npArrayD14, '#p_14':self.npArrayP14 })
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
            if self._filetype != "stderrLEv1":
                self._XDataInt = self._XData[index] * 100
                #print("self._XDataInt*100:", self._XDataInt)
                self._XDataInt = self._XDataInt.round(0)
                st = str((self._XDataInt).tolist())
                st = ''.join(st.replace('.0','').replace(',','').replace('[','').replace(']',''))
            else:
                st = str(self._XCol["#d_01"][index].round(0)) + " " + str(self._XCol["#p_01"][index])
                st += " " + str(self._XCol["#d_03"][index].round(0)) + " " + str(self._XCol["#p_03"][index])
                st += " " + str(self._XCol["#d_04"][index].round(0)) + " " + str(self._XCol["#p_04"][index])
                st += " " + str(self._XCol["#d_06"][index].round(0)) + " " + str(self._XCol["#p_06"][index])
                st += " " + str(self._XCol["#d_07"][index].round(0)) + " " + str(self._XCol["#p_07"][index])
                st += " " + str(self._XCol["#d_08"][index].round(0)) + " " + str(self._XCol["#p_08"][index])
                st += " " + str(self._XCol["#d_14"][index].round(0)) + " " + str(self._XCol["#p_14"][index])
        else:
            st ="0 0 0 0 0 0 0"

        st = ''.join(st.replace('.0', '').replace(',', '').replace('[', '').replace(']', ''))
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
