import os
import pickle

from tensorflow.keras import layers
from tensorflow.keras.models import Sequential


def make_dnn_regressor(in_shape = 10, 
                        hidden_sizes = [24,48,96,192,96,48,24,12], 
                        dropout = 0.2):
    """Code for constructing the dnn regressor, included for posterity/reference.

    Args:
        in_shape (int, optional): _description_. Defaults to 10.
        hidden_sizes (list, optional): _description_. Defaults to [24,48,96,192,96,48,24,12].
        dropout (float, optional): _description_. Defaults to 0.2.

    Returns:
        _type_: _description_
    """
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
    """_summary_

    Args:
        prediction_array (_type_): _description_

    Returns:
        _type_: _description_
    """    
    for i, x in enumerate(prediction_array):
        if x > 1.0:
            prediction_array[i] = 1.0
        elif x < 0.0:
            prediction_array[i] = 0.0
    return prediction_array


