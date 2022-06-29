import os
import pytest

from SalmonEuAdmix import allele_info, panel_snps
from SalmonEuAdmix.model import load_y_scaler, load_x_scaler, load_dnn, load_lite_dnn
from SalmonEuAdmix.encode import readPedMap_tsv_fmt, encode_ped, get_model_inputs, subset_snp_df


def test_ReadAndPredict():
    model = load_dnn()
    x_scaler = load_x_scaler()
    y_scaler = load_y_scaler()

    extra_ped_file = 'SalmonEuAdmix/data/unit_test2.ped'
    extra_map_file = 'SalmonEuAdmix/data/unit_test2.map'

    extra_snp_data, extra_snp_columns = readPedMap_tsv_fmt(extra_ped_file, extra_map_file)

    assert extra_snp_data.shape == (20, 533)
    assert len(extra_snp_columns) > 513

    extra_snp_data_513gts = subset_snp_df(extra_snp_data, panel_snps)

    #encode the data
    snp_data, _ = encode_ped(extra_snp_data_513gts, panel_snps, encoding_dict = allele_info)

    #get the ml inputs
    test_X, _ = get_model_inputs(snp_data, panel_snps, x_scaler = x_scaler)

    #make sure the inputs are expected shape
    assert test_X.shape == (20, 513)

    #make predictions with the model
    test_yht_raw = model.predict(test_X)

    #use y scaler to transform the outputs
    test_yht = y_scaler.inverse_transform(test_yht_raw)

    #Sand_12_* are Norwegian fish, so we expect 100%
    rounded_yht = [int(x) for x in test_yht]

    expected_preds = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0]