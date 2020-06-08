#https://machinelearningmastery.com/regression-tutorial-keras-deep-learning-library-python/

import time
import os
import sys
import logging
import argparse
from datetime import datetime

import pandas
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasRegressor
import keras.callbacks
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import numpy as np


####################
# handle arguments passed to the script
def handle_main_arg():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v","--verbose", help="enable verbosity mode ", action="store_true")
    args = parser.parse_args()
    #if args.verbose:
    #    logging.basicConfig(level=logging.INFO)
    #else:
    #    logging.basicConfig(level=logging.CRITICAL)

def loadX(filename):
     # load dataset
    dataframe = pandas.read_csv(filename, delimiter='\t', skipinitialspace=True , header=0)
    dataset = dataframe.values
    #columns = dataframe.columns
    #print(columns)
    XCol = dataframe[['#d_01', '#d_03', '#d_04', '#d_06', '#d_07', '#d_08', '#d_18']]
    XData = XCol.values
    #print(XData)
    return XData

def loadY(filename):
     # load dataset
    dataframe = pandas.read_csv(filename, delimiter='\t', skipinitialspace=True , header=0)
    YCol = dataframe[['#X True', '#Y True', '#Z True']]
    Ydata=YCol.values
    return Ydata

def prepareYdata(Ydata):
    #first step is to get rid of negative values
    minVal = Ydata.min(0)
    print("minVal:", minVal)
    YdataPrepared = Ydata + (-1*minVal)
    return YdataPrepared, minVal

def prepareCsv(filename):
    dataframe = pandas.read_csv(filename, delimiter='\t', skipinitialspace=True , header=0)
    dataset = dataframe.values
    XCol = dataframe[['#d_01', '#d_03', '#d_04', '#d_06', '#d_07', '#d_08', '#d_18']]
    YCol = dataframe[['#X True', '#Y True', '#Z True']]
    Ydata, minVal = prepareYdata(YCol.values)
    XCol.to_csv("XData.csv", sep='\t')
    pandas.DataFrame(Ydata, columns=YCol.columns).to_csv("YData.csv", sep='\t')
    return minVal

# define base model
def baseline_model():
    # create model
    model = Sequential()
    model.add(Dense(128, input_dim=7, kernel_initializer='normal', activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(16, activation='relu'))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(3, activation='relu'))
    #print(model.output_shape)
    print(model.summary())
    # Compile model
    model.compile(loss='mean_squared_error', optimizer='adam')
    return model

def exportModel(model, filename):
    #get_weights() for a Dense layer returns a list of two elements, the first element contains the weights, and the second element contains the biases. So you can simply do:
    # weights = model.layers[0].get_weights()[0]
    # biases = model.layers[0].get_weights()[1]

    weights = model.get_weights()
    #model_cfg = model.get_config()
    np.savetxt(filename , weights , fmt='%s', delimiter=',')
    model_json = model.to_json()
    #with open(filename, "w") as json_file:
    #    json_file.write(model_json)
    # serialize weights to HDF5
    #model.save_weights("model.h5")
    print("Saved model to disk")

def printDate():
    now = datetime.now()
    print(now.strftime("%Y/%m/%d %H:%M:%S"))

def testPredict(filename, minVal, estimator):
    prepareCsv(filename)
    Xdata = loadX("XData.csv")
    Ydata = loadY("YData.csv")
    predictions = estimator.predict(Xdata)
    for line in predictions:
        line = line + minVal
        print(line)

####################
def main():
    print ("Python version:"+sys.version)

    minVal = prepareCsv("./datas/Full.csv")

    Xdata = loadX("XData.csv")
    Ydata = loadY("YData.csv")
    #Ydata = loadY("datas/Test2_short.anl")
    #Ydata, minVal = prepareYdata(Ydata)
    print(Ydata)


    estimator = baseline_model()
    printDate()
    print("## Start training ##")
    tensorboard_callback = keras.callbacks.TensorBoard(log_dir="./logs")
    estimator.fit(Xdata, Ydata, epochs=5, batch_size=50, callbacks=[tensorboard_callback])
   
    #estimator = KerasRegressor(build_fn=baseline_model, epochs=10, verbose=0)
    #kfold = KFold(n_splits=5, shuffle=True)
    #scores = cross_val_score(estimator, Xdata, Ydata, cv=kfold)
    #print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
    #print(scores)

    printDate()
    print("## Training End ##")
    #exportModel(estimator, "exported_model.csv")

    estimator.fit(Xdata, Ydata, callbacks=[tensorboard_callback])

    testPredict("./datas/Test1_short.anl", minVal, estimator)
    testPredict("./datas/Test2_short.anl", minVal, estimator)

    try:
        while True:
            time.sleep(1)
                
    except KeyboardInterrupt:
        #logging.info("exiting")
        print("Exit on KeyboardInterrupt")

####################
if __name__ == "__main__":
    handle_main_arg()
    main()