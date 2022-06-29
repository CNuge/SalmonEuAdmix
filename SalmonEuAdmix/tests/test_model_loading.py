import os
import pytest
import numpy as np
from SalmonEuAdmix.model import load_y_scaler, load_x_scaler, load_dnn


def test_LoadScalers():    
    x_scaler = load_x_scaler()
    y_scaler = load_y_scaler()
 
    y_scaler.n_features_in_ == 1    #make sure it processes inputs of shape (,  1)
    x_scaler.n_features_in_ == 513  #make sure it processes inputs of shape (,513)


def test_LoadDNN():

    model = load_dnn()
    #check the input shape
    assert (model.input_details[0]['shape'] == np.array([1, 513])).all()
    #outputs single numbers
    assert (model.output_details[0]['shape'] == np.array([1, 1])).all()
    #and the outputs are floats
    assert model.output_details[0]['dtype'] == np.float32
