"""
SalmonEuAdmix: a machine learning-based library for estimating European admixture proportions in Atlantic salmon. 

==========
Data and models
==========

TODO - add descriptions here
"""

import os
import pickle

location = os.path.dirname(os.path.realpath(__file__))

allele_info_file = os.path.join(location, 'data', 'SNP_major_minor_info.pkl')
allele_info = pickle.load(open(allele_info_file, "rb"))
panel_snps = list(allele_info.keys())


#possibly: remove code below, use the model.py module code to instantiate the objects here
# or can leave that detail unabstracted

"""
x_scaler_file = os.path.join(location, 'data', 'X_scaler_v1')
y_scaler_file = os.path.join(location, 'data', 'y_scaler_v1')

print("make sure these agree, keep just one of the two for final")
dnn_file = os.path.join(location, 'data', 'DNNregressor_model_v1')
dnn_file_tflite = os.path.join(location, 'data', 'panel_dnn_tflite')


#init the scalers
x_scaler = pickle.load(open(x_scaler_file, "rb"))
y_scaler = pickle.load(open(y_scaler_file, "rb"))

#init the DNN model for predictions
#either
panel_dnn = pickle.load(open(dnn_file, "rb"))
#or
from SalmonEuAdmix.model import load_lite_dnn
panel_dnn = load_lite_dnn(dnn_file_tflite)

"""