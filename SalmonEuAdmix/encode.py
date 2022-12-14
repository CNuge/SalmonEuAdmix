import numpy as np
import pandas as pd

from SalmonEuAdmix import reduced_panel_snps


def readPedMap_tsv_fmt(ped_file, map_file, headers = False):
    """Read in a ped and map file and build a pandas DataFrame.

    Args:
        ped_file (str): The path and name of the plink ped file.
        map_file (str): The path and name of the plink map file.
        headers (bool, optional): Boolean indicating if the input ped and map files have header rows. Defaults to False.

    Returns:
        pandas.DataFrame: A pandas dataframe with the leading metadata columns and genotype data.
        list: A list of the names of the columns with the genotype data. 
    """
    col_names = ["chromosome", "snp" , "genetic_distance", "physical_distance"]
    if headers == True:
        #read in the map file
        map_data = pd.read_csv(map_file, skiprows = 0, names = col_names, delim_whitespace=True)
        #build the complete column name list
        header_data = ['#family', 'individual', 'sire', 'dam', 'sex', 'pheno']
        snp_columns = list(map_data['snp'].values)
        #read in the ped file and apply the headers
        snp_data = pd.read_csv(ped_file, skiprows = 0, header = None, delim_whitespace=True)
        #split the metadata columns from the front
        leading_cols = snp_data.loc[:, :5].set_axis(header_data, axis=1, inplace=False)
        #merge the two genotypes into a single space delimited column each
        gt_snp_data = pd.DataFrame(snp_data.loc[:, 6::2].astype(str).values + 
                                        ' ' +  snp_data.loc[:, 7::2].astype(str).values, 
                                    index=snp_data.index, columns=snp_columns)
        #join the leading columns to the snp columns and return
        snp_data = pd.concat([leading_cols, gt_snp_data], axis=1)
        return snp_data, snp_columns
    else:
        #read in the map file
        map_data = pd.read_csv(map_file, names = col_names, delim_whitespace=True)
        #build the complete column name list
        header_data = ['#family', 'individual', 'sire', 'dam', 'sex', 'pheno']
        snp_columns = list(map_data['snp'].values)
        #read in the ped file and apply the headers
        snp_data = pd.read_csv(ped_file, header = None, delim_whitespace=True)
        #split the metadata columns from the front
        leading_cols = snp_data.loc[:, :5].set_axis(header_data, axis=1, inplace=False)
        #merge the two genotypes into a single space delimited column each
        gt_snp_data = pd.DataFrame(snp_data.loc[:, 6::2].astype(str).values + 
                                        ' ' + snp_data.loc[:, 7::2].astype(str).values, 
                                    index=snp_data.index, columns=snp_columns)
        #join the leading columns to the snp columns and return
        snp_data = pd.concat([leading_cols, gt_snp_data], axis=1)
        return snp_data, snp_columns
  

def get_unique_alleles(gt_count_dict):
    """Determine the major and minor alleles for the given SNP marker.

    Args:
        gt_count_dict (dict): A dictonary where the genotypes are the keys, 
                                and their number of occurances are the values.

    Raises:
        ValueError: Error if a SNP has more than 2 alleles. Biallelic SNPs only. 
        ValueError: Error if a SNP has only one alleles. Monomorphic SNPs lack information. 

    Returns:
        (str, str): The major and minor alleles.
    """
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
    
        Used for imputing missing info.

    Args:
        snp_arr (np.array): An array of the SNP genotypes.

    Returns:
        str: The most common genotype in the input array.
    """

    vals, counts = np.unique(snp_arr, return_counts=True)
    index = np.argmax(counts)
    return vals[index]


def dosage_encode_snps(snp_arr, missing_val = "0 0", missing_replacement = None, 
                            record_snps = False, known_pq = None):
    """Dosage encode SNP genotypes for machine learning use.
    
    Homozygous for major allele encoded as 0, heterozygoous = 1, Homozygous minor allele = 2.

    Args:
        snp_arr (numpy.array): _description_
        missing_val (str, optional): The string used to encode missing values in the ped file. Defaults to "0 0".
        replace_missing_method (str, optional): _description_. Defaults to "mode".
        record_snps (bool, optional): Should the function return the dictonary of major and minor alleles. Defaults to False.
        known_pq (tuple, optional): The known major and minor alleles. Defaults to None.

    Raises:
        ValueError: If most common genotype is the missing genotype code, an error is thrown.
        ValueError: If the known major and minor alleles are passed, 
                    throw an error if more than two alleles are specified.

    Returns:
        list: Dosage encoded SNP data for the input genotype array.
    """
    if missing_replacement is None:
        mode_gt = calc_mode(snp_arr)
        if mode_gt == missing_val:
            raise ValueError("most common allele is a missing genotype!")
        snp_arr[snp_arr == missing_val] = mode_gt
    else:
        snp_arr[snp_arr == missing_val] = missing_replacement

    if known_pq is not None:
        #use the known major and minor alleles
        if len(known_pq) != 2:
            raise ValueError("tuple of known_pq must be made of two and only two characters.")
        p, q = known_pq['p'], known_pq['q']

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


def encode_ped(snp_data, snp_columns, 
                get_alleles = False, encoding_dict = None, imputation_info = None):
    """Take a string format PED and turn it into dosage encoding.

    Args:
        snp_data (pandas.DataFrame): The dataframe with string formatted genotypes.
        snp_columns (list): A list of strings specifying the marker names for encoding.
        get_alleles (bool, optional): Boolean flag indicating if the major and minor allele should be returned. 
                                        Defaults to False.
        encoding_dict (dict, optional): An optional dictonary of dictonaries with the known major and minor alleles 
                                        for the marker (format: {'snp_name': {'p': 'major_allele_character', 'q': 'minor_allele_character'}}). 
                                        Defaults to None (in which case MAF is determined de novo).
        imputation_info (dict, optional) : An optional dictonary providing replacement alleles for missing data if available.
                                            If not provided, the mean value from each column of snp_data will be used for imputation.

    Returns:
        pandas.DataFrame: A dosage encoded dataframe for use with the machine learning algorithm.
        dict: A dictonary of dictonaries with the major and minor alleles for the markers. 
             format: { 'snp_name': {'p': 'major_allele_character', 
                                    'q': 'minor_allele_character'} }. 
    """
    #make a copy of the input so that its not overriding the original, also prevents 
    #the pandas CopyWarning flag
    snp_data = snp_data.copy()
    #encode with known major and minor alleles
    if encoding_dict is not None:
        #x = snp_columns[5]
        for x in snp_columns:
            pq_info = encoding_dict[x]
            if imputation_info is None:
                snp_data[x], _ = dosage_encode_snps(snp_data[x].values, known_pq = pq_info, )
            else:
                missing_replacement = imputation_info[x]
                snp_data[x], _ = dosage_encode_snps(snp_data[x].values, known_pq = pq_info, 
                                                    missing_replacement = missing_replacement)

        return snp_data, None
    #calculate major and minor alleles from scratch, encode and return the major and minor dictonary
    elif get_alleles == True:
        allele_info = {}
        for x in snp_columns:
            #print(x)
            if imputation_info is None:
                snp_data[x], _ = dosage_encode_snps(snp_data[x].values, known_pq = pq_info)
            else:
                missing_replacement = imputation_info[x]
                snp_data[x], _ = dosage_encode_snps(snp_data[x].values, known_pq = pq_info, 
                                                    missing_replacement = missing_replacement)
            allele_info[x] = snp_dict
        return snp_data, allele_info
    #calculate major and minor alleles from scratch, encode but don't save the major and minor info
    else:
        #x = snp_columns[3]
        for x in snp_columns:
            #print(x)
            snp_data[x], _ = dosage_encode_snps(snp_data[x].values)
        return snp_data, None


def subset_snp_df(snp_df, subset_list, leading_cols = False):
    """Take a dataframe of SNPs, subset only the columns for the list of SNPs provided.
    
    Option to include the header data (default = False).

    Args:
        snp_df (pandas.DataFrame): A dataframe with the SNP information.
        subset_list (list): A list with the SNP column names to retain.
        leading_cols (bool, optional): Boolean indicating if the leading columns from a PED file be 
                                        retained along with the specified SNP columns. 
                                        Defaults to False.

    Returns:
        pandas.DataFrame: The dataframe with only the SNP columns specified by the input subset_list.
    """

    if leading_cols == False:
        try:
            return snp_df[subset_list]
        except KeyError:
            raise KeyError("Could not subset required markers from ped file,"+\
                " ensure that all required SNPs are present.")
    if leading_cols == True:
        header_data = ['#family', 'individual', 'sire', 'dam', 'sex', 'pheno']
        sub_merged = header_data + subset_list
        try:
            return snp_df[sub_merged]
        except KeyError:
            raise KeyError("Could not subset the required markers from ped file,"+\
                           " ensure that all required SNPs are present.")


def get_model_inputs(df, x_cols = reduced_panel_snps, y_col = None, x_scaler = None, y_scaler = None):
    """Subset the specified X and y columns from a pandas dataframe and conver to format
        required by the machine learning algorithms.

    Args:
        df (pandas.dataframe): A dataframe with the specified columns.
        x_cols (list, optional): The list of X columns to subset. Defaults to reduced_panel_snps.
        y_col (str, optional): The name of the y column to subset. Defaults to None.
        x_scaler (sklearn.StandardScaler, optional): A scaler to modify X the inputs. Defaults to None.
        y_scaler (sklearn.StandardScaler, optional): A scaler to modify y the inputs. Defaults to None.

    Returns:
        (np.array, np.array): Numpy arrays with the X and y data to pass to the neural network.
    """    
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


