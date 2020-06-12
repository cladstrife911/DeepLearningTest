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
import sklearn.metrics
import numpy as np

#class EarlyStoppingByLossVal(Callback):
#    def __init__(self, monitor='val_loss', value=0.00001, verbose=0):
#        super(Callback, self).__init__()
#        self.monitor = monitor
#        self.value = value
#        self.verbose = verbose

#    def on_epoch_end(self, epoch, logs={}):
#        current = logs.get(self.monitor)
#        if current is None:
#            warnings.warn("Early stopping requires %s available!" % self.monitor, RuntimeWarning)

#        if current < self.value:
#            if self.verbose > 0:
#                print("Epoch %05d: early stopping THR" % epoch)
#            self.model.stop_training = True

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
    i=1
    for layer in model.layers:
        np.savetxt("./output/W"+str(i)+".csv" , layer.get_weights()[0] , fmt='%s', delimiter=',')
        np.savetxt("./output/B"+str(i)+".csv" , layer.get_weights()[1] , fmt='%s', delimiter=',')
        i=i+1

    weights = model.get_weights()
    #model_cfg = model.get_config()
    np.savetxt(filename , weights , fmt='%s', delimiter=',')
    model_json = model.to_json()
    #with open(filename, "w") as json_file:
    #    json_file.write(model_json)
    # serialize weights to HDF5
    model.save_weights("model.h5")
    print("model saved to disk")

def printDate():
    now = datetime.now()
    print(now.strftime("%Y/%m/%d %H:%M:%S"))

def testPredict(filename, minVal, estimator):
    print("###################### testPredict ######################", minVal)
    prepareCsv(filename)
    Xdata = loadX("XData.csv")
    Ydata = loadY("YData.csv")
    predictions = estimator.predict(Xdata)
    #print("## testPredict ## minVal:", minVal)
    dataset_est = pandas.DataFrame({'#X Est': predictions[:, 0], '#Y Est': predictions[:, 1], '#Z Est': predictions[:, 2]})
    print("Estimated:", dataset_est)
    # Apply the initial correction on the real output
    Ydata =Ydata + (-1*minVal)
    dataset_real = pandas.DataFrame({'#X Real': Ydata[:, 0], '#Y Real': Ydata[:, 1], '#Z Real': Ydata[:, 2]})
    print("Real:", dataset_real)
    print("## mean_squared_error :", sklearn.metrics.mean_squared_error(dataset_real.values, dataset_est.values))
    print("## mean_absolute_error :", sklearn.metrics.mean_absolute_error(dataset_real.values, dataset_est.values))
    print("## median_absolute_error :", sklearn.metrics.median_absolute_error(dataset_real.values, dataset_est.values))
    print("## diff :", abs(dataset_real.values - dataset_est.values))


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
    callbacks = [
        keras.callbacks.EarlyStopping(monitor="loss", min_delta=0.0001, patience=3),
        #EarlyStoppingByLossVal(monitor='val_loss', value=0.5, verbose=1),
        # EarlyStopping(monitor='val_loss', patience=2, verbose=0),
        #ModelCheckpoint(kfold_weights_path, monitor='val_loss', save_best_only=True, verbose=0),
        keras.callbacks.TensorBoard(log_dir="./logs"),
    ]
    estimator.fit(Xdata, Ydata, epochs=100, batch_size=5, callbacks=callbacks)
   
    #estimator = KerasRegressor(build_fn=baseline_model, epochs=10, verbose=1)
    #kfold = KFold(n_splits=5, shuffle=True)
    #scores = cross_val_score(estimator, Xdata, Ydata, cv=kfold)
    #print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
    #print(scores)

    printDate()
    print("## Training End ##")
    exportModel(estimator, "exported_model.csv")

    estimator.fit(Xdata, Ydata)#, callbacks=[tensorboard_callback])

    testPredict("./datas/Test1_short.csv", minVal, estimator)
    testPredict("./datas/Test2_short.csv", minVal, estimator)

    print("## End of script ##")
    #try:
    #    while True:
    #        time.sleep(1)
                
    #except KeyboardInterrupt:
    #    #logging.info("exiting")
    #    print("Exit on KeyboardInterrupt")

####################
if __name__ == "__main__":
    handle_main_arg()
    main()