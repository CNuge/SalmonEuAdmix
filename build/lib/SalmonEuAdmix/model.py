import os
import pickle
import numpy as np
import pandas as pd

from tensorflow.keras import layers
from tensorflow.keras.models import Sequential


def make_dnn_regressor(in_shape = 10, 
                        hidden_sizes = [24,48,96,192,96,48,24,12], 
                        dropout = 0.2):

    """ Code for constructing the dnn regressor, included for posterity/reference."""
    #initiate the model
    model = Sequential()
    #specify the in layer, denoting size
    model.add(layers.Dense(in_shape, input_shape=(in_shape,) , activation = 'relu'))

    n_hidden = len(hidden_sizes)

    for i in range(0,n_hidden):
        model.add(layers.Dense(hidden_sizes[i], activation = 'relu'))
        if dropout != 0:
            model.add(layers.Dropout(dropout))

    model.add(layers.Dense(1, kernel_initializer='normal',activation='linear'))

    # Compile the network :
    model.compile(loss='mean_absolute_error', 
                    optimizer='adam', 
                    metrics=['mean_absolute_error'])

    return model


def load_x_scaler():
    """Load the X scaler used to prep data for the model input"""
    location = os.path.dirname(os.path.realpath(__file__))
    x_scaler_file = os.path.join(location, 'data', 'X_scaler_v1')
    x_scaler = pickle.load(open(x_scaler_file, "rb"))
    
    return x_scaler


def load_y_scaler():
    """Load the y scaler used to scale the outputs of the model (or to prep labels for model training)."""
    location = os.path.dirname(os.path.realpath(__file__))
    y_scaler_file = os.path.join(location, 'data', 'y_scaler_v1')
    y_scaler = pickle.load(open(y_scaler_file, "rb"))
    
    return y_scaler


def load_dnn():
    """Load the tensorflow lite version of the model"""
    location = os.path.dirname(os.path.realpath(__file__))
    dnn_file = os.path.join(location, 'data', 'DNNregressor_model_v1')
    panel_dnn = pickle.load(open(dnn_file, "rb"))

    return panel_dnn


def mask_outside_limits(prediction_array):
    for i, x in enumerate(prediction_array):
        if x > 1.0:
            prediction_array[i] = 1.0
        elif x < 0.0:
            prediction_array[i] = 0.0
    return prediction_array


if __name__ == '__main__':
    print("TODO - change this to functions and make it reusable, cleanup this section when done")    
    print(" decide if I need all the model code, I think good to include for posterity even if bloat")
    dpath = "data/"

    #load the scalers    
    x_scaler = pickle.load(open(dpath+"X_scaler_v1", "rb"))
    y_scaler = pickle.load(open(outpath+"y_scaler_v1", "rb"))

    #transform the inputs
    test_X = x_scaler.transform(test_X_raw)


    #load the model
    regr = pickle.load(open(dpath+"DNNregressor_model_v1", "rb"))
  
    #predict on the inputs
    test_yht_raw = regr.predict(test_X)

    #use y scaler to transform the outputs
    test_yht = y_scaler.inverse_transform(test_yht_raw)


    print("code to make it a tsv output, with the sample IDs and admixture percs")

    test_df = pd.DataFrame()
    test_df['DNN_predictions'] = test_yht
    test_df.to_csv(outpath+"DNN_predictions_test_samples.tsv", sep = '\t', index = False)

