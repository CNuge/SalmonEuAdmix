import os
import pickle

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential


def make_dnn_regressor(in_shape = 513, 
                        hidden_sizes = [1026, 342, 114], 
                        dropout = 0.2):
    """Code for constructing the dnn regressor, included for posterity/reference.

    The defaults are the the values that were used in the model construction.

    Args:
        in_shape (int, optional): Shape of the model input. Defaults to 513.
        hidden_sizes (list, optional): _description_. Defaults to [1026, 342, 114].
        dropout (float, optional): _description_. Defaults to 0.2.

    Returns:
        _type_: _description_
    """
    #initiate the model
    model = Sequential()
    #specify the in layer, denoting size
    model.add(layers.Dense(in_shape, input_shape=(in_shape,) , activation = 'relu'))
    n_hidden = len(hidden_sizes)
    #add in the hidden layers
    for i in range(0,n_hidden):
        model.add(layers.Dense(hidden_sizes[i], activation = 'relu'))
        if dropout != 0:
            model.add(layers.Dropout(dropout))
    #final dense layer for the output
    model.add(layers.Dense(1, kernel_initializer='normal',activation='linear'))
    # Compile the network :
    model.compile(loss='mean_absolute_error', 
                    optimizer='adam', 
                    metrics=['mean_absolute_error'])
    return model


def load_x_scaler():
    """Load the X scaler used to prep data for the model input."""
    location = os.path.dirname(os.path.realpath(__file__))
    x_scaler_file = os.path.join(location, 'data', 'X_scaler_v1')
    x_scaler = pickle.load(open(x_scaler_file, "rb"))
    return x_scaler


def load_y_scaler():
    """Load the y scaler used to scale the outputs of the model 
    (or to prep labels for model training)."""
    location = os.path.dirname(os.path.realpath(__file__))
    y_scaler_file = os.path.join(location, 'data', 'y_scaler_v1')
    y_scaler = pickle.load(open(y_scaler_file, "rb"))
    return y_scaler


def load_dnn():
    """Load the tensorflow lite version of the model."""
    location = os.path.dirname(os.path.realpath(__file__))
    dnn_file = os.path.join(location, 'data', 'dnn_513_tf.h5')
    panel_dnn = keras.models.load_model(dnn_file)    
    return panel_dnn

#panel_dnn = pickle.load(open('DNNregressor_model_v1', "rb"))
#panel_dnn.save('dnn_513_tf.h5')

def load_301_x_scaler():
    """Load the X scaler used to prep data for the model input."""
    location = os.path.dirname(os.path.realpath(__file__))
    x_scaler_file = os.path.join(location, 'data', 'X_scaler_v4')
    x_scaler = pickle.load(open(x_scaler_file, "rb"))
    return x_scaler


def load_301_y_scaler():
    """Load the y scaler used to scale the outputs of the model 
    (or to prep labels for model training)."""
    location = os.path.dirname(os.path.realpath(__file__))
    y_scaler_file = os.path.join(location, 'data', 'y_scaler_v4')
    y_scaler = pickle.load(open(y_scaler_file, "rb"))
    return y_scaler


def load_301_dnn():
    """Load the tensorflow lite version of the model."""
    location = os.path.dirname(os.path.realpath(__file__))
    dnn_file = os.path.join(location, 'data', 'dnn_301_tf.h5')
    panel_dnn = keras.models.load_model(dnn_file)    
    return panel_dnn

#panel_dnn = keras.models.load_model('dnn_301_tf/saved_model.pb')   
#panel_dnn = pickle.load(open('DNNregressor_model_v4', "rb"))
#panel_dnn.save('dnn_301_tf.h5')

def mask_outside_limits(prediction_array):
    """ Constrain the predictions to true proportions (between 0 and 1).

    Args:
        prediction_array (list or numpy.array): a set of predictions.

    Returns:
        list or numpy.array: format will match that of the input.
    """    
    for i, x in enumerate(prediction_array):
        if x > 1.0:
            prediction_array[i] = 1.0
        elif x < 0.0:
            prediction_array[i] = 0.0
    return prediction_array
