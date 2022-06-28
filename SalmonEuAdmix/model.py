import pickle
import pandas as pd

from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

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


import gc
import pickle
import numpy as np
import tensorflow as tf  
from tensorflow import lite

def save_model_with_signatures(trained_model_dir, output_dir):
	"""
	Save model with signatures
	:param trained_model_dir (str): path to saved model after training
	:param output_dir (str): path to save model with signatures
	Returns 
	None
	"""
	model = build_onoff_rnn(load_weights=trained_model_dir)
	run_model = tf.function(lambda x: model(x))
	
	BATCH_SIZE = 1
	STEPS = 21
	INPUT_SIZE = 5
	
	concrete_func = run_model.get_concrete_function(
		tf.TensorSpec([BATCH_SIZE, STEPS, INPUT_SIZE], model.inputs[0].dtype))
	
	model.save(output_dir, save_format="tf", signatures=concrete_func)
	return None


def convert_to_tflite_format(model_dir, lite_model_name):
	"""
	Convert full precision model to tflite format 
	:param model_dir (str) : path where model with signatures was saved
	:param lite_model_name (str) : filename of tflite model
	Returns: 
	None
	"""
	converter = tf.lite.TFLiteConverter.from_saved_model(model_dir)
	tflite_quant_model = converter.convert() 
	with open(lite_model_name, 'wb') as f:
		f.write(tflite_quant_model)
	return None


class Predictor(lite.Interpreter):
    def load_model_details(self):
        self.allocate_tensors()
        self.input_details = self.get_input_details()
        self.output_details = self.get_output_details()
    
    def predict(self, input):
        print('input shape', input.shape)
        self.set_tensor(self.input_details[0]["index"], np.array([input], dtype=np.float32))
        self.invoke()
        output_data = self.get_tensor(self.output_details[0]["index"])
        return np.argmax(output_data)


def load_lite_dnn(dnn_file_tflite):
    tf_lite_model = Predictor(dnn_file_tflite)
    tf_lite_model.load_model_details()
    tf_lite_model.reset_all_variables()
    return tf_lite_model

if __name__ == '__main__':


    print("TODO - change this to functions and make it reusable, cleanup this section when done")    
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

    tf_lite_file = dpath+"panel_dnn_tflite"
