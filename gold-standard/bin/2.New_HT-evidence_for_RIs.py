'''
NAME
      Identification of new HT-binding evidence from the RIs mapping to HT-peaks proccess

VERSION
       3.0

AUTHOR
       Paloma Lara <palomalf86@gmail.com>

DESCRIPTION

The program takes the RI file resulting from the TFBS mapping process against the peaks 
of HT datasets and identifies if the found evidence and references are new.
       
CATEGORY
       mapping programs

USAGE
       python 2.New_HT-evidence_for_RIs.py

ARGUMENTS
    none

SOFTWARE REQUERIMENTS
    python 3.11
    libraries: os, pandas

INPUT
     RISet.txt file mapped containing the additional "Evidence;Referencecolumns" and "matchingpeaks"
     (the output file from the script "1.RIs_mapping_To_HT-TF-binding-datasets.py")

OUTPUT
     An RISet_mapped.txt file with three additional columns: "Evidence;Reference", "matchingpeaks" and "New (Evidence:reference)"

CREATION DATE
     30/06/2023

'''
import os
import pandas as pd

### Config/setting section ### 
pd.set_option('display.max_columns',20)
pd.set_option('display.max_rows',50)

# The path project contains data-input, bin, results directories
basePath= "./"

# The paths to the RIs-mapped file 
riMappedFilePath = basePath + "results/RI_mapping_to_TFBS-HT/TFRIs_RDB12.0_Risv2.0_mapped.txt"
dfRiMapped= pd.read_csv(riMappedFilePath, sep="\t", comment='#', header=0)

# The paths for the outputfiles
outputFilePath= basePath + "results/RI_mapping_to_TFBS-HT/New_ev_TF-RISet_12.0_v2.0.txt"
outputFile = open(outputFilePath,"w")

###
print("Start")

# Write the column names in the output file
risColumnsNamesArrays = dfRiMapped.columns.values
risColumnsNamesList = list(risColumnsNamesArrays)
riColumnNames=""
for c in risColumnsNamesList:
    riColumnNames += (c + "\t")   
print(riColumnNames)
outputColumNames= riColumnNames + "New (Evidence:reference)" + "\n"
outputFile.write(outputColumNames)

print("RIs Mapped shape")
print(dfRiMapped.shape)

counter=0
counterB=0

# loop through each row of the RIs dataframe 
for index, row in dfRiMapped.iterrows():

    #Save the complete RI row as a string 
    riLine0=row
    riLine=""
    for a in riLine0:
        b= str(a)
        riLine += (b + "\t")  
    print(riLine)

    counter+=1
    print(counter)

    #Create a vector for the new evidence-references
    evsRefsNew = []

    # TFBS Evidence and Reference in RegulonDB
    tfrsEvidences = row['21)tfrsEvidence']
    tfrsEvidence=str(tfrsEvidences)
    riEvidences= row['22)riEvidence']
    riEvidence= str(riEvidences)

    # HT Evidence and Reference from mapping process 
    htEvidence = row['Evidence;Reference']
    htEvidenceString=str(htEvidence)

    # The RI maps with more than one evidence
    if "), (" in htEvidenceString:
        print("yes")
        htEvidenceVector=htEvidenceString.split("), (")
        monitor=0

       # Get each evidence and its properties
        for i in htEvidenceVector:
            singleEvidence1=i
            singleEvidence2=singleEvidence1.replace("(", "")
            singleEvidence3=singleEvidence2.replace(")", "")
            singleEvidenceVector=singleEvidence3.split(";")
            singleEvidenceCode=singleEvidenceVector[0]
            print(singleEvidenceCode)

            #This is the most important step for determain if the evidence is new or not
            # Check if the HT-Evidence Code is not in RegulonDB TFBS and RI evidence 
            if (singleEvidenceCode not in  tfrsEvidence) and (singleEvidenceCode not in riEvidence):
                newSingleEvidence= "("+str(singleEvidence3)+")"
                newSingleEvidenceS= newSingleEvidence.replace(";", ":")
                evsRefsNew.append(newSingleEvidenceS)
    else: 
        singleEvidence=htEvidenceString.replace("(", "")
        singleEvidence=singleEvidence.replace(")", "")
        singleEvidenceVector=singleEvidence.split(";")
        singleEvidenceCode=singleEvidenceVector[0]
        monitor=0

        if (singleEvidenceCode not in  tfrsEvidence) and (singleEvidenceCode not in  riEvidence):
            newSingleEvidence= "("+str(singleEvidence)+")"
            newSingleEvidenceS= newSingleEvidence.replace(";", ":")
            evsRefsNew.append(newSingleEvidenceS) 


    # Formatting the new evidence and reference 
    evsRefsNew2= str(evsRefsNew)
    evsRefsNew3= evsRefsNew2.replace("[", "")
    evsRefsNew4= evsRefsNew3.replace("]", "")
    evsRefsNewString= evsRefsNew4.replace("'", "")

    # Write in the output file the current RI with the new evidences and refreneces 
    outputLine1=(str(riLine) + str(evsRefsNewString)+ "\n") 
    outputFile.write(outputLine1)
    counterB+=1
    print("counterB",counterB)

outputFile.close()
print("End")
