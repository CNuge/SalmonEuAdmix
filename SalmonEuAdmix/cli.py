from multiprocessing.sharedctypes import Value
import sys
import argparse
import pandas as pd
from SalmonEuAdmix import allele_info, panel_snps, mode_gts, reduced_panel_snps
from SalmonEuAdmix.model import load_y_scaler, load_x_scaler, load_dnn, mask_outside_limits
from SalmonEuAdmix.model import load_301_y_scaler, load_301_x_scaler, load_301_dnn 
from SalmonEuAdmix.encode import readPedMap_tsv_fmt, encode_ped, get_model_inputs, subset_snp_df


def input_parser(args):
    parser  = argparse.ArgumentParser(prog = "SalmonEuAdmix",
        description = """
        SalmonEuAdmix:\n
        a command line tool for estimating European admixture proportions in Atlantic salmon.
        """)
    parser.add_argument("-p", "--ped", type = str,  
        help = "The ped file of genotypes for individuals to predict.")
    parser.add_argument("-m", "--map", type = str,
        help = "The map file corresponding to the ped file.")
    parser.add_argument("-o", "--out", type = str , default = "admix_pred.tsv", 
        help = "The name output file that is produced.")
    parser.add_argument("-c", "--constrain", type = bool , default = True, 
        help = "Boolean indicating if program should constrain the predicted proportions\n"+\
            "to lower bound of 0.0 and upper bound of 1.0. Default is True.")
    parser.add_argument("-n", "--neuralnetwork", type = str , default = '301_model', 
        help = "String indicating which predictive model (deep neural network)\n"+\
            "should be used to make the admixture predictions.\n"+\
            "Two options are available: \n"+\
            "'301_model' - indicates the 301 SNP model should be used.\n"+\
            "'513_model' - indicates the 513 SNP model should be used.\n"+\
            "\n"+\
            "Default is the smaller 301-SNP model.")

    return parser.parse_args(args)


def main():
    #parse the command line inputs
    parsed_args = input_parser(sys.argv[1:])
    ped_file = parsed_args.ped
    map_file = parsed_args.map
    out_file = parsed_args.out
    constrain = parsed_args.constrain
    model_selection = parsed_args.neuralnetwork    
    print("loading the ped file")
    #make sure necessary data was provided
    if ped_file == None:
        raise ValueError("must specify an input ped file with the flag -p")
    if map_file == None:
        raise ValueError("must specify an input map file with the flag -m")
    #load the ped file & map file using code in encode
    snp_data, snp_columns = readPedMap_tsv_fmt(ped_file, map_file)
    individuals = snp_data['individual']
    if model_selection == "513_model":
        print("loading the 513 SNP model")
        panel_dnn = load_dnn()
        x_scaler = load_x_scaler()
        y_scaler = load_y_scaler()
        #make sure the 513 markers present, subset if excess SNPs present
        if len(snp_columns) < 513:
            raise ValueError("input ped file must contain the 513 snps of the marker panel. see: panel_513_data.map for list")
        elif len(snp_columns) > 513:
            print("input contained more than 513 SNPs, subsetting the 513 panel snps from larger file")
            snp_data = subset_snp_df(snp_data, panel_snps)
        else:
            print("input contained 513 SNPs")
        print("encoding the inputs")
        #encode the data
        snp_data, _ = encode_ped(snp_data, panel_snps, encoding_dict=allele_info, imputation_info=mode_gts)
        #get the ml inputs
        test_X, _ = get_model_inputs(snp_data, panel_snps, x_scaler=x_scaler)
        print("making predictions")
        #make predictions with the model
        test_yht_raw = panel_dnn.predict(test_X)
        #use y scaler to transform the outputs
        test_yht = y_scaler.inverse_transform(test_yht_raw)
        #mask predictions >1. or less than 0.
        if constrain == True:
            test_yht = mask_outside_limits(test_yht)
        print("saving to file")
        #build the output dataframe
        out_df = pd.DataFrame({'individual' : individuals})
        out_df['EuAdmix_Proportion'] = test_yht
        #save data to the specified output file
        out_df.to_csv(out_file, sep = '\t', index = False)
        print("done!") 
    elif model_selection == "301_model":
        print("loading the 301 SNP model")
        panel_dnn = load_301_dnn()
        x_scaler = load_301_x_scaler()
        y_scaler = load_301_y_scaler()
        #make sure the 513 markers present, subset if excess SNPs present
        if len(snp_columns) < 301:
            raise ValueError("input ped file must contain the 301 snps of the marker panel. see: panel_301_data.map for list")
        elif len(snp_columns) > 301:
            print("input contained more than 301 SNPs, subsetting the 301 panel snps from larger file")
            snp_data = subset_snp_df(snp_data, reduced_panel_snps)
        else:
            print("input contained 301 SNPs")

        print("encoding the inputs")
        #encode the data
        snp_data, _ = encode_ped(snp_data, reduced_panel_snps, encoding_dict=allele_info, imputation_info=mode_gts)
        #get the ml inputs
        test_X, _ = get_model_inputs(snp_data, reduced_panel_snps, x_scaler=x_scaler)
        print("making predictions")
        #make predictions with the model
        test_yht_raw = panel_dnn.predict(test_X)
        #use y scaler to transform the outputs
        test_yht = y_scaler.inverse_transform(test_yht_raw)
        #mask predictions >1. or less than 0.
        if constrain == True:
            test_yht = mask_outside_limits(test_yht)
        print("saving to file")
        #build the output dataframe
        out_df = pd.DataFrame({'individual' : individuals})
        out_df['EuAdmix_Proportion'] = test_yht
        #save data to the specified output file
        out_df.to_csv(out_file, sep = '\t', index = False)
        print("done!") 
    else:
        raise ValueError(f"The neuralnetwork (-n) param must be either: 301_model or 513_model")

if __name__ == '__main__':
    main()
