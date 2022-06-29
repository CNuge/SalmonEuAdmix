import pickle
import numpy as np
import pandas as pd

from SalmonEuAdmix import panel_snps


def readPedMap_tsv_fmt(ped_file, map_file = "", headers = False):
    
    col_names = ["chromosome", "snp" , "genetic_distance", "physical_distance"]

    if headers == True:
        map_data = pd.read_csv(map_file, skiprows = 0, names = col_names, sep = '\t')
        
        header_data = ['#family', 'individual', 'sire', 'dam', 'sex', 'pheno']
        snp_columns = list(map_data['snp'].values)
        header_data.extend(snp_columns)

        snp_data = pd.read_csv(ped_file, skiprows = 0, names = header_data, sep = '\t')
        return snp_data, snp_columns
        
    else:
        
        map_data = pd.read_csv(map_file, names = col_names, sep = '\t')
        
        header_data = ['#family', 'individual', 'sire', 'dam', 'sex', 'pheno']
        snp_columns = list(map_data['snp'].values)
        header_data.extend(snp_columns)
        
        snp_data = pd.read_csv(ped_file, names = header_data, sep = '\t')
        return snp_data, snp_columns



def get_unique_alleles(gt_count_dict):
    """Determine the major and minor alleles for the given SNP marker."""
    unique_alleles = {}
    for x in gt_count_dict.keys():
        for a in x.split(" "):
            if a in unique_alleles.keys():
                unique_alleles[a] = unique_alleles[a] + gt_count_dict[x]
            else:
                unique_alleles[a] = gt_count_dict[x]
    if len(unique_alleles) > 2:
        raise ValueError("SNP is not biallelic")
    if len(unique_alleles) == 1:
        raise ValueError("SNP is homozygous")
    k1, k2 = unique_alleles.keys()
    if unique_alleles[k1] >= unique_alleles[k2]:
        return k1, k2
    else:
        return k2, k1


def calc_mode(snp_arr):
    """Get the most common value in the array of SNP values. 
    
    Used for imputing missing info."""
    vals, counts = np.unique(snp_arr, return_counts=True)
    index = np.argmax(counts)
    return vals[index]



#  snp_arr = snp_data[x].values
#' Homozygous for major allele encoded as 0, heterozygoous = 1, Homozygous minor allele = 2
#' method - make it so you can do one hot, dosage, or presence/absence. currently just dosage
#' missing_data - can put in the mode or NA
def dosage_encode_snps(snp_arr, missing_val = "0 0", replace_missing_method = "mode", 
                            record_snps = False, known_pq = False):
    """"""
    if replace_missing_method == "mode" :
        mode_gt = calc_mode(snp_arr)
        if mode_gt == missing_val:
            raise ValueError("most common allele is a missing genotype!")

        snp_arr[snp_arr == missing_val] = mode_gt
    
    if known_pq == True:
        #use the known major and minor alleles
        if len(known_pq) != 2:
            raise ValueError("tuple of known_pq must be made of two and only two characters.")
        p, q = known_pq

    else:
        #determine the major and minor alleles
        vals, counts = np.unique(snp_arr, return_counts=True)
        gt_count_dict = {k : v for k, v in zip(vals, counts)}

        p, q = get_unique_alleles(gt_count_dict)
 
    encodings = {f"{p} {p}" : 0,
                    f"{p} {q}" : 1,
                    f"{q} {p}" : 1,
                    f"{q} {q}" : 2}

    encoded_data = [encodings[x] for x in snp_arr] 

    if record_snps == True:
        outdict = {'p' : p , 'q' : q}
        return encoded_data, outdict

    return encoded_data, None


def encode_ped(snp_data, snp_columns, get_alleles = False, encoding_dict = None):
    """ Take a string format PED and turn it into dosage encoding."""

    #make a copy of the input so that its not overriding the original, also prevents 
    #the pandas CopyWarning flag
    snp_data = snp_data.copy()
    
    #encode with known major and minor alleles
    if encoding_dict is not None:
        #x = snp_columns[5]
        for x in snp_columns:
            pq_info = encoding_dict[x]
            #print(x)
            snp_data[x], _ = dosage_encode_snps(snp_data[x].values, known_pq = pq_info)
        return snp_data, None

    #calculate major and minor alleles from scratch, encode and return the major and minor dictonary
    elif get_alleles == True:
        allele_info = {}
        for x in snp_columns:
            #print(x)
            snp_data[x], snp_dict = dosage_encode_snps(snp_data[x].values, record_snps = True)
            allele_info[x] = snp_dict

        return snp_data, allele_info

    #calculate major and minor alleles from scratch, encode but don't save the major and minor info
    else:
        #x = snp_columns[3]
        for x in snp_columns:
            #print(x)
            snp_data[x], _ = dosage_encode_snps(snp_data[x].values)
        return snp_data, None


#snp_df = extra_snp_data
#subset_list = list(allele_info.keys())
def subset_snp_df(snp_df, subset_list, leading_cols = False):
    """Take a dataframe of SNPs, subset only the columns for the list of SNPs provided.
    
    Option to include the header data (default = False)."""
    if leading_cols == False:
        return snp_df[subset_list]
    if leading_cols == True:
        header_data = ['#family', 'individual', 'sire', 'dam', 'sex', 'pheno']
        sub_merged = header_data + subset_list
        return snp_df[sub_merged]

#df = train_df
def get_model_inputs(df, x_cols = panel_snps, y_col = None, x_scaler = None, y_scaler = None):
    """ """
    #get the x values
    x_out = np.array(list(df[x_cols].values))
    #if an X scaler is passed, transform the X values using it
    if x_scaler is not None:
        x_out = x_scaler.transform(x_out)
    #get the y values
    if y_col is None:
        y_out = None
    else:
        y_out = df[y_col].values
        #if a y scaler is passed and there are y values, transform the y values using it
        if y_scaler is not None:
            y_out = y_scaler.transform(np.expand_dims(y_out, axis=1))
            y_out = np.squeeze(y_out)
    return x_out, y_out


if __name__ == '__main__':

    dpath = "data/"

    allele_info = pickle.load(open(dpath+"SNP_major_minor_info.pkl", "rb"))

    ped_file = dpath+'panel_513_data.ped'
    map_file = dpath+'panel_513_data.map'
    snp_data, snp_columns = readPedMap_tsv_fmt(ped_file, map_file)

    assert snp_columns == list(allele_info.keys()) #can use this for subsetting a bigger ped

    extra_ped_file = dpath+'unit_test2.ped'
    extra_map_file = dpath+'unit_test2.map'
    extra_snp_data, extra_snp_columns = readPedMap_tsv_fmt(extra_ped_file, extra_map_file)

    assert len(snp_columns) == 513
    assert len(extra_snp_columns) > 513

    extra_snp_data = subset_snp_df(extra_snp_data, list(allele_info.keys()))
    assert len(extra_snp_columns) == 513

    snp_data, _ = encode_ped(snp_data, snp_columns, encoding_dict = allele_info)

    """
    test the other methods

    snp_data, snp_columns = readPedMap_tsv_fmt(ped_file, map_file)
    snp_data, _ = encode_ped(snp_data, snp_columns)

    snp_data, allele_info = encode_ped(snp_data, snp_columns, get_alleles = True)
    assert len(allele_info.keys()) == len(snp_columns)

    """

