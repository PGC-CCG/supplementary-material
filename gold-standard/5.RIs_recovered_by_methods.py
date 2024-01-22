'''
NAME
      RIs recovered by HT methods
VERSION
       1.0

AUTHOR
       Paloma Lara <palomalf86@gmail.com>

DESCRIPTION
       This program allows the analysis of RIs (the total set or a subset, for instance the classical or confirmed RIs) are recovered in the datasets from each HT TF-binding collection (ChIP-seq, ChIP-exo, DAP-seq and gSELEX). 
       
CATEGORY
       Mapping programs

USAGE
       Program [OPTIONS]

ARGUMENTS

SOFTWARE REQUIREMENTS

INPUT
     TF-RISet.txt download from https://regulondb.ccg.unam.mx/datasets, with or without a filter process 

OUTPUT
   RIs_mapped_counts.xlsx, this file contains the total of RIs recovered by each methodology (ChIP-seq, ChIP-exo, DAP-seq and gSELEX)
   DAP-SEQ_counts_by_TF.txt, this file contains the number of RIs recovered for each TF in the DAP-seq collection
   GSELEX_counts_by_TF.txt, this file contains the number of RIs recovered for each TF in the gSELEX collection
   CHIP-SEQ_counts_by_TF.txt, this file contains the number of RIs recovered for each TF in the ChIP-seq collection
   CHIP-EXO_counts_by_TF.txt, this file contains the number of RIs recovered for each TF in the ChIP-exo collection
     
CREATION DATE
     30/07/2023

'''

import pandas as pd

# List of input file names, which have the list of TFs that have at least a dataset for the corresponding methodology
inputFiles = [
    "DAP-SEQ",
    "GSELEX",
    "CHIP-SEQ",
    "CHIP-EXO"
]

# Dictionary to store results
results = {}

# Process each input file
for method in inputFiles:
    # Read TFs file into a DataFrame
    dfTfs = pd.read_excel("/Volumes/GoogleDrive/Shared drives/PGC-02.Proyectos_vigentes/Curacion/Curación_HT_pl/curation_datasets-HT/3.Desarrollo/DatasetsTFBSRegulonDB11.2/metodology_benchmarch/input/"+method+".xlsx")

    # Read "RIs_set.xlsx" file into a DataFrame, selecting columns of interest
    dfRis = pd.read_excel("/Volumes/GoogleDrive/Shared drives/PGC-02.Proyectos_vigentes/Curacion/Curación_HT_pl/curation_datasets-HT/3.Desarrollo/DatasetsTFBSRegulonDB11.2/metodology_benchmarch/input/RIs_mapped.xlsx", usecols=["4)regulatorName", "21)tfrsEvidence", "Evidence;Reference"])
    dfRis.fillna("", inplace=True)

    outputFileCountsByTfPath = "/Volumes/GoogleDrive/Shared drives/PGC-02.Proyectos_vigentes/Curacion/Curación_HT_pl/curation_datasets-HT/3.Desarrollo/DatasetsTFBSRegulonDB11.2/metodology_benchmarch/output/"+method+"_counts_by_TF.txt"
    outputFileCountsByTf = open(outputFileCountsByTfPath, "w")
    # Filter rows in dfRis where "TFRI" is in "TF" of dfTfs
    risTfsFromInput = dfRis[dfRis["4)regulatorName"].isin(dfTfs["TF"])]

    # Get the total number of RIs in the analyzed set that exist for the group of TFs  analyzed 
    numRisTfInputTotal = len(risTfsFromInput)

    # Count the number of rows containing the method name in "HT-evidence" column
    numRisTfInputDetected = len(risTfsFromInput[(risTfsFromInput["Evidence;Reference"].str.contains(str(method)))])

    # Count the number of different strings in the "TFRI" column
    numDifferentStringsTfriInput = len(risTfsFromInput["4)regulatorName"].unique())

    # Calculate the percentage of recovered RIs by the corresponding methodology for the group of TFs analized
    percentageRecovered = (numRisTfInputDetected / numRisTfInputTotal) * 100

    # Store the results in the dictionary
    results[method] = {
        "NumEvaluatedTFs": numDifferentStringsTfriInput,
        "NumRIsFromEvaluatedTFs": numRisTfInputTotal,
        "NumRIsRecovered": numRisTfInputDetected,
        "%RIsRecovered": percentageRecovered  # New percentage column
    }
    #For each methodology (or colecction of HT TF-binding datasets), counts the number of RIs recovered by TF
    columnRegulator = risTfsFromInput['4)regulatorName']
    uniqueValues = columnRegulator.unique().tolist()
    dfRisByTF = pd.DataFrame()
    for value in uniqueValues:
        filterRis = dfRis['4)regulatorName'] == value
        dfRisByTF = dfRis[filterRis]
        numRisByTFTotal = len(dfRisByTF)
        numRisByTFMapped = len(dfRisByTF[(dfRisByTF["Evidence;Reference"].str.contains(str(method)))])
        percentRisRecoveredByTF = (numRisByTFMapped / numRisByTFTotal * 100)
        outputLine = str(value) + "\t" + str(numRisByTFTotal) + "\t" + str(numRisByTFMapped) + "\t" + str(percentRisRecoveredByTF) + "\n"
        outputFileCountsByTf.write(outputLine)

# Create a DataFrame from the results (total of RIs recovered) dictionary
dfResults = pd.DataFrame(results).T

# Save the results to an output file
dfResults.to_excel("/Volumes/GoogleDrive/Shared drives/PGC-02.Proyectos_vigentes/Curacion/Curación_HT_pl/curation_datasets-HT/3.Desarrollo/DatasetsTFBSRegulonDB11.2/metodology_benchmarch/output/RIs_mapped_counts.xlsx", indexLabel="Method")