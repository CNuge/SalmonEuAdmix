import pickle

import numpy as np
import pandas as pd

from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from sklearn.preprocessing import StandardScaler


def make_dnn_regressor(in_shape = 10, 
                        hidden_sizes = [24,48,96,192,96,48,24,12], 
                        dropout = 0.2):

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





if __name__ == '__main__':


    print("TODO - change this to functions and make it reusable")    
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
