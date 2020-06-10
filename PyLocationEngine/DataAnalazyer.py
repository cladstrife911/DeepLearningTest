import os
import pandas

class DataAnalyzer:
    _XCol = []
    _YCol = []
    _gOffsetvalue = 40
    _gOffsetActive = False
    _gNumberOfSample = 0

    # TODO: make the list of d_x configurable
    def __init__(self, filename):
        self.dataframe = pandas.read_csv(filename, delimiter='\t', skipinitialspace=True , header=0)
        self._XCol = self.dataframe[['#d_01', '#d_03', '#d_04', '#d_06', '#d_07', '#d_08', '#d_18']]
        self._YCol = self.dataframe[['#X True', '#Y True', '#Z True']]
        self._XData = self._XCol.values
        self._YData = self._YCol.values
        self.fn = filename
        self._gNumberOfSample = self.dataframe.shape[0]
        #print("# of sample in file:", self._gNumberOfSample)

    def getNumberOfSamples(self):
        return self._gNumberOfSample

    # Get X values (used as input for deep learning)
    def getXs(self):
        return self._XData

    # Return one line of XData converted into string int*100
    def getSerializedX(self, index):
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
