import sys
import argparse

from SalmonEuAdmix import allele_info, panel_snps, panel_dnn, x_scaler, y_scaler
from SalmonEuAdmix.encode import readPedMap_tsv_fmt, encode_ped, get_model_inputs

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
	#parse the command line inputs
    parsed_args = input_parser(sys.argv[1:])
    ped_file = parsed_args.ped
    map_file = parsed_args.map
    out_file = parsed_args.out
	#make sure necessary data was provided
    if ped_file == None:
        raise ValueError("must specify an input ped file with the flag -p")
    if map_file == None:
        raise ValueError("must specify an input map file with the flag -m")
    #load the ped file & map file using code in encode
    snp_data, snp_columns = readPedMap_tsv_fmt(ped_file, map_file)
	#make sure the 513 markers present, subset if excess SNPs present
    if len(snp_columns) < 513:
        raise ValueError("input ped file must contain the 513 snps of the marker panel. see: panel_513_data.map for list")
    elif len(snp_columns) > 513:
        snp_data = subset_snp_df(snp_data, panel_snps)
    #encode the data
    snp_data, _ = encode_ped(snp_data, snp_columns, encoding_dict = allele_info)
    #get the ml inputs
    test_X, _ = get_model_inputs(snp_data, panel_snps, x_scaler = x_scaler)
    #make predictions with the model
    test_yht_raw = panel_dnn.predict(test_X)
    #use y scaler to transform the outputs
    test_yht = y_scaler.inverse_transform(test_yht_raw)
    #build the output dataframe
    out_df = pd.DataFrame({'individual' : snp_data['individual']})
    out_df['EuAdmix_Proportion'] = test_yht
    #save data to the specified output file
    out_df.to_csv(out_file, sep = '\t', index = False)


if __name__ == '__main__':
    main()