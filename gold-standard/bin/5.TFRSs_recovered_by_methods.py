'''
NAME
      TFRSs recovered by HT methods
VERSION
       1.0

AUTHOR
       Paloma Lara <palomalf86@gmail.com>

DESCRIPTION
       This program allows the analysis of TFRSs from RIs (the total set or a subset, 
       for instance the classical or confirmed RIs) are recovered in the datasets 
       from each HT TF-binding collection (ChIP-seq, ChIP-exo, DAP-seq and gSELEX). 
       
CATEGORY
       Mapping programs

USAGE
       Program [OPTIONS]

ARGUMENTS

SOFTWARE REQUIREMENTS
       python
       libraries: pandas

INPUT
     TF-RISet.txt download from https://regulondb.ccg.unam.mx/datasets, with or without a filter process 

OUTPUT
   DAP-SEQ_sites_counts_by_TF.txt, this file contains the number of TFRSs recovered for each TF in the DAP-seq collection
   GSELEX_sites_counts_by_TF.txt, this file contains the number of TFRSs recovered for each TF in the gSELEX collection
   CHIP-SEQ_sites_counts_by_TF.txt, this file contains the number of TFRSs recovered for each TF in the ChIP-seq collection
   CHIP-EXO_sites_counts_by_TF.txt, this file contains the number of TFRSs recovered for each TF in the ChIP-exo collection
     
CREATION DATE
     30/07/2023

'''
import pandas as pd

# List of input file names
input_files = [
    "DAP-SEQ",
    "GSELEX",
    "CHIP-SEQ",
    "CHIP-EXO"
]

# Dictionary to store results
results = {}

# Process each input file
for method in input_files:
    # Read the TFs file into a DataFrame
    df_tfs = pd.read_excel("./input/" + method + ".xlsx")

    # Read the "RIs_set.xlsx" file into a DataFrame, selecting columns of interest
    df_ris = pd.read_excel("./input/TF-RISet_12.1_CV_without_HT_mapped_confirmed.xlsx")
    df_ris.fillna("", inplace=True)
    output_file_counts_by_tf_path = "./output/" + method + "_sites_counts_by_TF.txt"
    output_file_counts_by_tf = open(output_file_counts_by_tf_path, "w")
    output_line0 = "TF" + "\t" + "Num_Sites_Classical" + "\t" + "Num_Sites_recovered" + "\t" + "Percent_Sites_Recovered_by_TF" + "\n"
    output_file_counts_by_tf.write(output_line0)
    
    # Filter rows in df_ris where "TFRI" is in df_tfs "TF"
    ris_tfs_from_input = df_ris[df_ris["4)regulatorName"].isin(df_tfs["TF"])]

    regulator_column = ris_tfs_from_input['4)regulatorName']
    unique_values = regulator_column.unique().tolist()
    df_ris_by_tf = pd.DataFrame()
    
    for value in unique_values:
        filter_condition = df_ris['4)regulatorName'] == value
        df_ris_by_tf = df_ris[filter_condition]
        
        # Keep only values from the "6)tfrsID" column and remove duplicates
        unique_tfrs_ids = df_ris_by_tf['6)tfrsID'].unique()
        
        # Get the number of unique values in the "6)tfrsID" column
        num_sites_by_tf_total = len(unique_tfrs_ids)

        ris_by_tf_mapped = df_ris_by_tf[
            df_ris_by_tf["Evidence;Reference"].str.contains(str(method))
        ]
        
        unique_tfrs_ids_mapped = ris_by_tf_mapped['6)tfrsID'].unique()
        num_sites_by_tf_mapped = len(unique_tfrs_ids_mapped)
        percent_sites_recovered_by_tf = (num_sites_by_tf_mapped / num_sites_by_tf_total * 100)
        
        output_line = str(value) + "\t" + str(num_sites_by_tf_total) + "\t" + str(num_sites_by_tf_mapped) + "\t" + str(percent_sites_recovered_by_tf) + "\n"
        output_file_counts_by_tf.write(output_line)

output_file_counts_by_tf.close()
