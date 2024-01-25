'''
NAME
       TFBS mapping to peaks from HT-TF binding collection

VERSION
       4.0

AUTHOR
       Paloma Lara <palomalf86@gmail.com>

DESCRIPTION
    The program allows for the mapping or searching of TF Binding Sites (TFBS) from RegulonDB 
    in collections of binding site files from different HT (high-throughput) technologies. 
    The goal is to determine how many of these HT-TFBS already exist in RegulonDB.

    The input data includes: 
    a) Annotated RIs from RegulonDB, where the known TFBS is included.
    b) Metadata describing each dataset 
    from each HT-binding collection. Each row in the metadata corresponds to a dataset and includes 
    information such as the TF name, data file name, experimental conditions, etc. 
    c) Directories containing the datasets for each HT-binding collection. Each collection has a 
    directory containing the data files for each experiment. Each file provides the results 
    of the experiment, such as peak coordinates, sequence, nearby gene, etc.

    The program maps the known TFBS (TF + binding site) from RegulonDB to each dataset in the 
    HT-binding collection to identify any matching peaks or sites (same TF and the peak is inside of the 
    coordinates of the known TFBS positions).

CATEGORY
       mapping programs

USAGE
       python tfbs-mapping.py 

ARGUMENTS

SOFTWARE REQUERIMENTS
    python 3.11
    libraries: os, pandas

INPUT

    The program requires:

     a) TF-RISet.txt file (https://regulondb.ccg.unam.mx/datasets)
     b) Metadata files (.xlsx) from all four HT_TFBSs collections 
     c) Four Directories with all datasets for each collection

OUTPUT
     An RISet_mapped.txt file containing two additional columns "Evidence;Reference" and "matchingpeaks"

CREATION DATE
     30/06/2023
     24/01/2024 checking by Hely

'''

import os
import pandas as pd

### Config/setting section ### 
pd.set_option('display.max_columns',20)
pd.set_option('display.max_rows',50)

# The path project contains data-input, bin, results directories
basePath= "./"

# Paths for ht-datasets collection 
chipexoPath = basePath + "data-input/ChIP-exo/Dataset_author_files/ChIP-exo_v4.0(tf-gene_mapped)/"
chipseqPath = basePath + "data-input/ChIP-seq/Dataset_author_files/ChIP-seq_v4.0(tf-gene_mapped)/"
dapseqPath  = basePath + "data-input/DAP-seq/Dataset_author_files/DAP-seq_v4.0(tf-gene_mapped)/"
gselexPath  = basePath + "data-input/gSELEX/Dataset_author_files/gSELEX_v4.0(tf-gene_mapped)/"

# Paths for metadata files of ht-datasets collections
chipexoMetPath = basePath + "data-input/ChIP-exo/metadata/DatasetCollection-TFBS-HT_ChIP-exo_RDB11.2.xlsx"
chipseqMetPath = basePath + "data-input/ChIP-seq/metadata/DatasetCollection-TFBS-HT_ChIP-seq_RDB11.2.xlsx"
dapseqMetPath  = basePath + "data-input/DAP-seq/metadata/DatasetCollection-TFBS-HT_DAP-seq_RDB11.2.xlsx"
gselexMetPath  = basePath + "data-input/gSELEX/metadata/DatasetCollection-TFBS-HT_gSELEX_RDB11.2.xlsx"

# Setting Collection names of HT-TFBSs
allCollections= ["Chipseq", "Chipexo", "Gselex", "Dapseq"]

### 
print("Start")

# Read the regulatory interactions file (RISet)
riFilePath  = basePath + "data-input/downloads/TF-RISet_12.1.txt"
dfRi= pd.read_csv(riFilePath, sep="\t", comment='#', header=0)
dfRi.columns = dfRi.columns.str.replace(' ', '')
dfRi = dfRi.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# Read the metadata file of each collection:  dfMetChipexo, dfMetChipseq, dfMetGselex, dfMetDapseq 
dfMetChipexo=pd.read_excel(chipexoMetPath, sheet_name="DATASET", comment='#', header=0)
dfMetChipseq=pd.read_excel(chipseqMetPath, sheet_name="DATASET", comment='#', header=0)
dfMetGselex=pd.read_excel(gselexMetPath, sheet_name="DATASET", comment='#', header=0)
dfMetDapseq=pd.read_excel(dapseqMetPath, sheet_name="DATASET", comment='#', header=0)

# Create the output files
outputFilePath= basePath + "results/RI_mapping_to_TFBS-HT/TF-RISet_12.1_mapped.txt"
errorOutputFilePath= basePath + "results/RI_mapping_to_TFBS-HT/Error_ClassConfwithoutHTdatasets_without_coords_v0.2_RDB12.1.txt"
outputFile = open(outputFilePath,"w")
errorOutputFile1 = open(errorOutputFilePath,"w")

# Write the column names in the output file
risColumnsNamesArrays = dfRi.columns.values
risColumnsNamesList = list(risColumnsNamesArrays)
riColumnNames=""
for c in risColumnsNamesList:
    riColumnNames += (c + "\t")   
print(riColumnNames)
outputColumNames = riColumnNames + "Evidence;Reference" + "\t" + "matchingpeaks" + "\n"
outputFile.write(outputColumNames)

# Filter the RIset, must remain only RIs with site with positions for the mapping process.
dfRi['7)tfrsLeft'] = pd.to_numeric(dfRi['7)tfrsLeft'], errors='coerce')
dfRis = dfRi[dfRi['7)tfrsLeft'].notna()]
print("RIs shape")
print(dfRi.shape)

# loop through the RIs dataframe
for index, row in dfRis.iterrows():
    #Save the complete RI row as a string 
    riLine0 = row
    riLine=""

    for a in riLine0:
        b= str(a)
        riLine += (b + "\t")  

    print(riLine)
    riTf = row['4)regulatorName']

    # Calculate the RI site center position
    riSiteStart = int(row['7)tfrsLeft'])
    riSiteEnd = int(row['8)tfrsRight'])
    length= riSiteEnd-riSiteStart
    riCenter= riSiteStart + (length/2)
    print(length)
    print(riCenter)
    
    # To start with the mapping:
    # Vector to save all evidence-references of peaks matching with ach RI
    evsRefs = []
    
    # Vector to save the data of peaks matching with ach RI
    matchingPeaks= []

    # If RI - site has position then mapping with ht-datasets
    if (riSiteStart!="-"):

        # loop through the elements of the vector allCollections
        for collection in allCollections:

            if collection == "Chipseq":   # check: refactoring these conditions with a dictionary -hso
                currentMetadata= dfMetChipseq
                evidenceCode = "EXP-CHIP-SEQ"
                currentDirPath= chipseqPath

            if collection == "Chipexo":
                currentMetadata= dfMetChipexo
                evidenceCode = "EXP-CHIP-EXO"
                currentDirPath= chipexoPath
            
            if collection == "Gselex":
                evidenceCode = "EXP-GSELEX"
                currentMetadata= dfMetGselex
                currentDirPath= gselexPath
            
            if collection == "Dapseq":
                evidenceCode = "EXP-DAP-SEQ"
                currentMetadata= dfMetDapseq
                currentDirPath= dapseqPath

            print(collection)
            #filter the current metadata to obtain only rows were the TF match with the TF of the current RI.
            filteredMetadata= currentMetadata[currentMetadata["RegulonDB TF Name"]==riTf]

            #Ignore for the mapping proccess datasets from gSELEX that have not cut off
            if collection == "Gselex":   # check: these filters doing when the medatada is loaded. line:65 -hso
                filteredMetadata= filteredMetadata[filteredMetadata["RegulonDB TF Name"]!="IHF"]
                filteredMetadata= filteredMetadata[filteredMetadata["RegulonDB TF Name"]!="H-NS"]
                filteredMetadata= filteredMetadata[filteredMetadata["RegulonDB TF Name"]!="Fis"]
                filteredMetadata= filteredMetadata[filteredMetadata["RegulonDB TF Name"]!="Lrp"]

            print("Ri_TF: ", riTf)
            print(currentMetadata.shape)
            print(filteredMetadata.shape)

            # loop through each row of the filtered metadata of the current collection to compare each dataset with the same TF of the current RI 
            for i, row in filteredMetadata.iterrows():
                fileName= row['Dataset File Name']
                pmidCell= str(row['PMID'])
                pmid=pmidCell.replace(".0", "")
                print("PMID: ", pmid)

                # only if filename exist, the mapping can continue
                if pd.notna(fileName):
                    evidenceReference = "("+str(evidenceCode)+";"+str(pmid)+")"

                    #load in a dataframe the data in the file corresponding to the current file name
                    currentDatasetPath = str(currentDirPath)+str(fileName)
                    dfCurrentDataset = pd.read_excel(currentDatasetPath, comment='#', header=0)

                    #loop through each row of the current dataset assigning the variables peakTfMainName, peakStart, peakEnd, peakCenter, peakMaximumCoverage, 
                    for j, row in dfCurrentDataset.iterrows():
                        peakTfMainName= row['TF Main Name']
                        pStart= row['Peak_start']
                        pEnd= row['Peak_end']
                        peakCenter= row['Peak center']
                        peakMaximumCoverage= row['Peak Maximum Coverage Position']
                        peakIntensity= row['Peak Intensity Fold Change/Binding intensity (%)']
                        peakType="x"

                        #If the row have peak start and peak end:
                        if pd.notna(pStart):
                            peakStart=pStart
                            peakEnd=pEnd
                            peakType= "a"
                        else:
                            #If the row have not peak start and peak end but have peak center:
                            if pd.notna(peakCenter):
                                if peakCenter != "NOT FOUND":
                                    peakStart = peakCenter - 100 # this value by argument or variable in the config section -hso
                                    peakEnd = peakCenter + 100
                                    peakType= "b"
                                else: 
                                    peakStart= 0
                                    peakEnd= 0
                                    peakType= "f"
                            else:
                                #If the row have not peak start and peak or peak center but have peak maximum coverage:
                                if pd.notna(peakMaximumCoverage):
                                    peakStart= peakMaximumCoverage-100
                                    peakEnd= peakMaximumCoverage+100
                                    peakType= "c"
                                else: 
                                    #If the row have not peak start and peak end or peak center or peak maximum coverage:
                                    errorOutputLine= (str(fileName) + "\t" + str(pmid) +"\n")
                                    errorOutputFile1.write(errorOutputLine)
                                    peakType= "d"
                            
                        fileNamePeakStart ="("+str(evidenceCode)+ ":" +str(fileName)+":"+str(peakStart)+ "-" + str(peakEnd)+ ":"+ str(peakType)+ ":" +str(peakIntensity)+")"
                        
                        # Mapping of the current RI to the current peak
                        if (riTf== peakTfMainName) & (riCenter > peakStart) & (riCenter < peakEnd):
                            print("yes")
                            matchingPeaks.append(fileNamePeakStart)
                            if evidenceReference not in evsRefs:
                                evsRefs.append(evidenceReference)   
                        
       # Modify the format of the data of evidence-reference and matching peaks        
        evsRefs2= str(evsRefs)
        evsRefs3= evsRefs2.replace("[", "")
        evsRefs4= evsRefs3.replace("]", "")
        evsRefsString= evsRefs4.replace("'", "")
        matchingPeaks2= str(matchingPeaks)
        matchingPeaks3= matchingPeaks2.replace("[", "")
        matchingPeaks4= matchingPeaks3.replace("]", "")
        matchingPeaksString= matchingPeaks4.replace("'", "")

        # Add to current RI the new evidences and references and the peaks matching
        outputLine1=(str(riLine) + str(evsRefsString) + "\t" + str(matchingPeaksString)+ "\n") 
        outputFile.write(outputLine1)
    else: 
        # The TFBS has not position to do the mapping therefore print null in matching columns
        outputLine2= (str(riLine) + "\t" + "\n")
        outputFile.write(outputLine2)

outputFile.close()
print("End")

