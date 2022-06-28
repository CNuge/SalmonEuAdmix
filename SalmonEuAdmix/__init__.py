"""
SalmonEuAdmix: a machine learning-based library for estimating European admixture proportions in Atlantic salmon. 

==========
Data and models
==========

TODO - add description here
"""


import os
import pickle

location = os.path.dirname(os.path.realpath(__file__))

x_scaler_file = os.path.join(location, 'data', 'X_scaler_v1')
y_scaler_file = os.path.join(location, 'data', 'y_scaler_v1')
allele_info_file = os.path.join(location, 'data', 'SNP_major_minor_info.pkl')
dnn_file = os.path.join(location, 'data', 'DNNregressor_model_v1')
 

x_scaler = pickle.load(open(x_scaler_file, "rb"))
y_scaler = pickle.load(open(y_scaler_file, "rb"))
panel_dnn = pickle.load(open(dpath+"DNNregressor_model_v1", "rb"))
allele_info = pickle.load(open(allele_info_file, "rb"))
panel_snps = list(allele_info.keys())
