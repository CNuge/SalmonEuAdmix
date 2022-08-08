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

mode_gt_file = os.path.join(location, 'data', 'SNP_impute_info.pkl')
mode_gts = pickle.load(open(mode_gt_file, "rb"))

reduced_marker_301_file = os.path.join(location, 'data', 'reduced_marker_list.pkl')
reduced_panel_snps = pickle.load(open(reduced_marker_301_file, "rb"))
## for dev:
# reduced_marker_301_file = 'SalmonEuAdmix/data/reduced_marker_list.pkl'

