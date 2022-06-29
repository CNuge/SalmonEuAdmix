import os
import pytest

from SalmonEuAdmix import allele_info, panel_snps
from SalmonEuAdmix.encode import readPedMap_tsv_fmt, subset_snp_df, encode_ped


def test_AlleleInfo():

    assert len(allele_info.keys()) == 513
    assert len(panel_snps) == 513

    for x in allele_info.keys():
        assert x in panel_snps


def test_PedMapReadAndTrim():

    std_ped_file = 'SalmonEuAdmix/data/panel_513_data.ped'
    std_map_file = 'SalmonEuAdmix/data/panel_513_data.map'

    snp_data_513, snp_columns_513 = readPedMap_tsv_fmt(std_ped_file, std_map_file)

    assert snp_data_513.shape == (20, 519)
    assert len(snp_columns_513) == 513
    assert panel_snps == snp_columns_513

    extra_ped_file = 'SalmonEuAdmix/data/unit_test2.ped'
    extra_map_file = 'SalmonEuAdmix/data/unit_test2.map'

    extra_snp_data, extra_snp_columns = readPedMap_tsv_fmt(extra_ped_file, extra_map_file)

    assert extra_snp_data.shape == (20, 533)
    assert len(extra_snp_columns) > 513

    extra_snp_data_513gts = subset_snp_df(extra_snp_data, panel_snps)
    assert extra_snp_data_513gts.shape == (20, 513)

    #lead cols variant
    with_header_extra_snp_data_513gts = subset_snp_df(extra_snp_data, panel_snps, leading_cols = True)
    assert with_header_extra_snp_data_513gts.shape == (20, 519)


def test_ReadAndEncode():
    
    extra_ped_file = 'SalmonEuAdmix/data/unit_test2.ped'
    extra_map_file = 'SalmonEuAdmix/data/unit_test2.map'

    extra_snp_data, extra_snp_columns = readPedMap_tsv_fmt(extra_ped_file, extra_map_file)

    assert extra_snp_data.shape == (20, 533)
    assert len(extra_snp_columns) > 513

    extra_snp_data_513gts = subset_snp_df(extra_snp_data, panel_snps)

    snp_data, _ = encode_ped(extra_snp_data_513gts, panel_snps, encoding_dict = allele_info)

