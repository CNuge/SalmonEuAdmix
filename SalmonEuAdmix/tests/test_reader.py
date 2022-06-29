import os
import pytest


from SalmonEuAdmix import allele_info, panel_snps
from SalmonEuAdmix.encode import readPedMap_tsv_fmt, subset_snp_df


def test_AlleleInfo():

    assert len(allele_info.keys()) == 513

    for x in len(allele_info.keys()):
        assert x in panel_snps

def test_PedMapReadAndTrim():

    std_ped_file = 'SalmonEuAdmix/data/panel_513_data.ped'
    std_map_file = 'SalmonEuAdmix/data/panel_513_data.map'

    snp_data_513, snp_columns_513 = readPedMap_tsv_fmt(std_ped_file, std_map_file)


    extra_ped_file = 'SalmonEuAdmix/data/unit_test2.ped'
    extra_map_file = 'SalmonEuAdmix/data/unit_test2.map'

    extra_snp_data, extra_snp_columns = readPedMap_tsv_fmt(extra_ped_file, extra_map_file)
