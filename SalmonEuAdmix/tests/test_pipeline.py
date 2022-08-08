from SalmonEuAdmix import allele_info, panel_snps, mode_gts
from SalmonEuAdmix.model import load_y_scaler, load_x_scaler, load_dnn 
from SalmonEuAdmix.encode import readPedMap_tsv_fmt, encode_ped, get_model_inputs, subset_snp_df


def test_ReadAndPredict():
    model = load_dnn()
    x_scaler = load_x_scaler()
    y_scaler = load_y_scaler()
    # the example files with superfluous and essential data columns
    extra_ped_file = 'SalmonEuAdmix/data/unit_test2.ped'
    extra_map_file = 'SalmonEuAdmix/data/unit_test2.map'
    # read the data in.
    extra_snp_data, extra_snp_columns = readPedMap_tsv_fmt(extra_ped_file, extra_map_file)
    # make sure the shapes are what is expected
    assert extra_snp_data.shape == (20, 533)
    assert len(extra_snp_columns) > 513
    # pull the required columns from the complete dataframe
    extra_snp_data_513gts = subset_snp_df(extra_snp_data, panel_snps)
    # encode the data
    snp_data, _ = encode_ped(extra_snp_data_513gts, panel_snps, 
                             encoding_dict = allele_info, imputation_info = mode_gts)
    # get the ml inputs
    test_X, _ = get_model_inputs(snp_data, panel_snps, x_scaler = x_scaler)
    # make sure the inputs are expected shape
    assert test_X.shape == (20, 513)
    # make predictions with the model
    test_yht_raw = model.predict(test_X)
    # use y scaler to transform the outputs
    test_yht = y_scaler.inverse_transform(test_yht_raw)
    # Sand_12_* are Norwegian fish, so we expect 100% Nor admixture pred for 
    # fish 10 - 17. Checking against rounded values to avoid floating point nuances
    # influencing the unit tests.
    rounded_yht = [int(x) for x in test_yht]
    expected_preds = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0]
    # ensure the rounded predictions match the expected predictions
    # this test *should* be robust to minor model changes.
    assert rounded_yht == expected_preds


# TODO - add unit tests and make nexessary code modifications to allow for 
# the different DNN (v4, trained on 301 SNP subset)
# to be swapped in and used.