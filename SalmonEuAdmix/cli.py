import sys
import argparse
import numpy as np

import pickle
from SalmonEuAdmix.encode import readPedMap_tsv_fmt, encode_ped

from SalmonEuAdmix import regression_dnn, x_scaler, y_scaler

def input_parser(args):
	parser  = argparse.ArgumentParser(prog = "SalmonEuAdmix",
		description = """
		SalmonEuAdmix:\n
		a command line tool for estimating European admixture proportions in Atlantic salmon.
		""")
	parser.add_argument("-p", "--ped", type = str,  
		help = "The ped file of genotypes for individuals to predict.\n"+\
		"ped: '.ped'\n")
	parser.add_argument("-m", "--map", type = str,
		help = "The map file corresponding to the ped file.")
	parser.add_argument("-o", "--out", type = str , default = "admix_pred.tsv", 
		help = "The name output file that is produced.")

	return parser.parse_args(args)



def main():

	parsed_args = input_parser(sys.argv[1:])

	ped_file = parsed_args.ped
	map_file = parsed_args.map
	out_file = parsed_args.out


	if ped_file == None:
		raise ValueError("must specify an input ped file with the flag -p")

	if map_file == None:
		raise ValueError("must specify an input map file with the flag -m")


	#load the ped file & map file using code in encode

	#encode the data

	#load the model

	#make predictions with the model

	#build the output dataframe

	#save data to the outfile




if __name__ == '__main__':
	main()