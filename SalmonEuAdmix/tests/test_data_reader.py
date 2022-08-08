import pytest
import numpy as np
from SalmonEuAdmix import allele_info, panel_snps, mode_gts
from SalmonEuAdmix.encode import readPedMap_tsv_fmt, subset_snp_df, encode_ped, dosage_encode_snps


def test_AlleleInfo():
    """ Test for the data structures in the package.
    """    
    assert len(allele_info.keys()) == 513
    assert len(panel_snps) == 513
    # make sure the allele dict and the panel list match
    for x in allele_info.keys():
        assert x in panel_snps


def test_PedMapReadAndTrim():
    """Test that the data are read in, and the marker panels are pulled and used.
    """
   # the example files with only the essential data columns
    std_ped_file = 'SalmonEuAdmix/data/panel_513_data.ped'
    std_map_file = 'SalmonEuAdmix/data/panel_513_data.map'
    # read in the data
    snp_data_513, snp_columns_513 = readPedMap_tsv_fmt(std_ped_file, std_map_file)
    # make sure the shapes are what is expected
    assert snp_data_513.shape == (20, 519)
    assert len(snp_columns_513) == 513
    assert panel_snps == snp_columns_513
    # the example files with superfluous and essential data columns
    extra_ped_file = 'SalmonEuAdmix/data/unit_test2.ped'
    extra_map_file = 'SalmonEuAdmix/data/unit_test2.map'
    # read in the data
    extra_snp_data, extra_snp_columns = readPedMap_tsv_fmt(extra_ped_file, extra_map_file)
    # make sure the shapes are what is expected
    assert extra_snp_data.shape == (20, 533)
    assert len(extra_snp_columns) > 513
    # pull the required columns from the complete dataframe
    extra_snp_data_513gts = subset_snp_df(extra_snp_data, panel_snps)
    assert extra_snp_data_513gts.shape == (20, 513)
    #lead cols variant
    with_header_extra_snp_data_513gts = subset_snp_df(extra_snp_data, panel_snps, leading_cols = True)
    assert with_header_extra_snp_data_513gts.shape == (20, 519)


def test_ReadAndEncode():
    """Test the encoding of the data frame
    """        
    extra_ped_file = 'SalmonEuAdmix/data/unit_test2.ped'
    extra_map_file = 'SalmonEuAdmix/data/unit_test2.map'

    extra_snp_data, extra_snp_columns = readPedMap_tsv_fmt(extra_ped_file, extra_map_file)

    assert extra_snp_data.shape == (20, 533)
    assert len(extra_snp_columns) > 513

    extra_snp_data_513gts = subset_snp_df(extra_snp_data, panel_snps)

    snp_data, _ = encode_ped(extra_snp_data_513gts, panel_snps, encoding_dict = allele_info)


def test_fails_ReadButEncodeFlagsMissingData():
    """Test that reading a file with missing columns fails
    """

    ped_file_301_markers = 'SalmonEuAdmix/data/panel_301_markers.ped'
    map_file_301_markers = 'SalmonEuAdmix/data/panel_301_markers.map'

    missing_snp_data, missing_snp_columns = readPedMap_tsv_fmt(ped_file_301_markers, map_file_301_markers)

    with pytest.raises(KeyError):
        missing_snp_data_301gts = subset_snp_df(missing_snp_data, panel_snps)


def test_missing_data_catch():

    snp_data_1 = np.array(["0 0", "0 0", "0 0", "0 0", "0 0", "A A",  "A T", "T T"])

    with pytest.raises(ValueError):
        dosage_encode_snps(snp_data_1)

    #it should work if we use the saved data
    fake_name = 'AX-87433461'
    mr = mode_gts[fake_name]
    out, _ = dosage_encode_snps(snp_data_1, missing_replacement=mr)

    assert out == [0, 0, 0, 0, 0, 2, 1, 0]