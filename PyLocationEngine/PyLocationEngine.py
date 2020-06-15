#https://machinelearningmastery.com/regression-tutorial-keras-deep-learning-library-python/

# How to run a training:
# => python PyLocationEngine.py -f=".\\datas\\Full.csv" -e=1
# How to test a model
# => python PyLocationEngine.py -m=".\\models\\20200615-18-20-32_model.h5" -t=".\\datas\\Full.csv"

import time
import os
import sys
import logging
import argparse
from datetime import datetime

import pandas
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from keras.models import Model
from keras.models import Sequential
from keras.models import load_model
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasRegressor
import keras.callbacks
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
import sklearn.metrics
import numpy as np

## Global variables ###
gArgs = []

####################
# handle arguments passed to the script
def handle_main_arg():
    global gArgs
    parser = argparse.ArgumentParser()
    parser.add_argument("-v","--verbose", help="enable verbosity mode ", action="store_true")
    parser.add_argument("-m","--model", help="path to existing model to load (h5 format)")
    parser.add_argument("-f","--filename", help="input file for training")
    parser.add_argument("-t","--testdata", help="input file for testing")
    parser.add_argument("-e","--epochs", help="epoch to run for the training")
    gArgs = parser.parse_args()
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

#It is required to apply an offset on Y data before the training because
# keras doesn't support negative value for regression model
# apply True when called before training, False to restore default value
def applyTrainingOffset(Ydata, apply):
    if apply:
        data = Ydata + 40
    else:
        data = Ydata - 40
    return data

def loadY(filename):
     # load dataset
    dataframe = pandas.read_csv(filename, delimiter='\t', skipinitialspace=True , header=0)
    YCol = dataframe[['#X True', '#Y True', '#Z True']]
    Ydata=YCol.values
    return Ydata

# define base model
def baseline_model():
    # create model
    model = Sequential()
    model.add(Dense(128, input_dim=7, kernel_initializer='normal', activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(16, activation='relu'))
    model.add(Dense(3, activation='relu'))
    #print(model.output_shape)
    print(model.summary())
    # Compile model
    model.compile(loss='mean_squared_error', optimizer='adam')
    return model

def exportModel(model, filename):
    #get_weights() for a Dense layer returns a list of two elements, 
    #the first element contains the weights, 
    #and the second element contains the biases.
    i=1
    for layer in model.layers:
        np.savetxt("./output/W"+str(i)+".csv" , layer.get_weights()[0] , fmt='%s', delimiter=',')
        np.savetxt("./output/B"+str(i)+".csv" , layer.get_weights()[1] , fmt='%s', delimiter=',')
        i=i+1
    timestamp = (datetime.now()).strftime("%Y%m%d-%H-%M-%S")
    weights = model.get_weights()
    #print("model.summary():",model.summary())
    model_json = model.to_json()
    writeFile("./models/"+timestamp+"_model_cfg.txt", model_json)
    model.save_weights("./models/"+timestamp+"_model.h5")
    print("model saved to disk")

def writeFile(filename, data):
    f = open(filename, "w")
    f.write(data)
    f.close()

def printDate():
    now = datetime.now()
    print(now.strftime("%Y/%m/%d %H:%M:%S"))

def testPredict(filename, model):
    print("###################### testPredict ######################")
    #Read and prepare input data
    Xdata = loadX(filename)
    #Estimate the position
    predictions = model.predict(Xdata)
    Yest = pandas.DataFrame({'#X Est': predictions[:, 0], '#Y Est': predictions[:, 1], '#Z Est': predictions[:, 2]})
    Yest = applyTrainingOffset(Yest, False)
    Yest.index.name='#nb'
    print("Estimated:", Yest)
    #Read the real position (from the trimble)
    Ydata = loadY(filename)
    Yreal = pandas.DataFrame({'#X Real': Ydata[:, 0], '#Y Real': Ydata[:, 1], '#Z Real': Ydata[:, 2]})
    Yreal.index.name='#nb'
    print("Real:", Yreal)
    #Compare estimated and real
    print("## mean_squared_error :", sklearn.metrics.mean_squared_error(Yreal.values, Yest.values))
    print("## mean_absolute_error :", sklearn.metrics.mean_absolute_error(Yreal.values, Yest.values))
    print("## median_absolute_error :", sklearn.metrics.median_absolute_error(Yreal.values, Yest.values))
    print("## diff :", abs(Yreal.values - Yest.values))
    #export the result to csv file
    ready_to_export_dataset = Yreal.join(Yest) 
    ready_to_export_dataset.to_csv("result_ets_real.csv", sep=';')

####################
def main():
    global gArgs
    print ("Python version:"+sys.version)

    if gArgs.filename:
        Xdata = loadX(gArgs.filename)
        Ydata = loadY(gArgs.filename)
        print("Ydata Raw:", Ydata)
        Ydata = applyTrainingOffset(Ydata,True)
        print("Ydata with Offset:",Ydata)

    # Define the model
    model = baseline_model()
    if gArgs.model:
        print("## loading model:", gArgs.model)
        model.load_weights(gArgs.model)
    else:
        #train a new model
        printDate()
        print("## Start training ##")
        callbacks = [
            keras.callbacks.EarlyStopping(monitor="loss", min_delta=0.0001, patience=3),
            keras.callbacks.TensorBoard(log_dir="./logs"),
        ]
        model.fit(Xdata, Ydata, epochs=int(gArgs.epochs), batch_size=5, callbacks=callbacks)
   
        #estimator = KerasRegressor(build_fn=baseline_model, epochs=10, verbose=1)
        #kfold = KFold(n_splits=5, shuffle=True)
        #scores = cross_val_score(estimator, Xdata, Ydata, cv=kfold)
        #print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
        #print(scores)
        #estimator.fit(Xdata, Ydata)

        printDate()
        print("## Training End ##")
        exportModel(model, "exported_model.csv")

    if gArgs.testdata:
        testPredict(gArgs.testdata, model)

    print("## End of script ##")

####################
if __name__ == "__main__":
    handle_main_arg()
    main()