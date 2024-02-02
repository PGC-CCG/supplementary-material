# *A Gold Standard for Transcription Factor Regulatory Interactions in Escherichia coli K-12: Architecture of Evidence Types*

Here, we present a detailed  analysis of the sources of knowledge supporting the collection of transcriptional regulatory interactions (RIs) of *E. coli K-12*. An RI groups the transcription factor, its effect (positive or negative)  and the regulated  target, a promoter, a gene or transcription unit. 

We improved the evidence codes so that  specific methods are incorporated , and  classified  into independent groups. On this basis we  updated the computation of confidence levels, weak, strong, or confirmed, for the collection of RIs. 

This process enriched the evidence of close to one quarter of RIs in RegulonDB release 11.1. Based on the new computational capabilities of our improved annotation of evidence sources, we can now analyze the internal architecture of evidence, their categories (experimental, classical, HT, computational), and confidence levels. 


## Requirements

The analyses of the anatomy of RI knowledge presented here were performed using 

- R (2022.06.23, version 4.2.1), 
- Rstudio (2022.07.1, Build 554), and the ggplot2 (version 3.4.0) library
- Python release 3.11 

All scripts and computational processes built to generate the data and analyses presented in this analysis are:
 
1. Run_Coordinate-Updates.py
2. 1.RIs_mapping_To_HT-TF-binding-datasets.py
3. 2.New_HT-evidence_for_RIs.py
4. 3.RIs_anatomy_analysis.R
5. 4.RIs_confidence_level_analysis.R
6. 5.TFRSs_recovered_by_methods.py
7. 6.Statistical_analysis.R


### 1. Annotation of HT evidence to RIs from RegulonDB based on the HT TF-binding datasets collection

The collection of  HT TF-binding datasets contains four subcollections with different number of TFs: DAP-seq, ChIP-seq, ChIP-exo, and gSELEX. The RIs from RegulonDB were mapped to this collection of datsets to add the cooresponding evidence types. 

#### 1.1 Uniformization of the genome coordinates for all datasets. 
In order to make these collections comparable among them and with RegulonDB TFRSs from RIs, the genome coordinates for all datasets were updated to the last genome version of the E. coli str. K-12 substr. MG1655 (U00096.3): 

The coordinates of the DAP-seq datasets were published using the last genome version of the E. coli str. K-12 substr. MG1655 (U00096.3), so they were not modified. The ChIP-seq, gSELEX, and ChIP-exo datasets with coordinates in the past genome version (U00096.2) were updated to version U00096.3. 

Program: Run_Coordinate-Updates.py

#### 1.2 To map the RegulonDB RI set with peaks from the HT-TFBSs subcollections.

A program in Python was implemented that compared each RI binding site with each peak corresponding to the same TF.  A match is assumed when the RI site coordinate is within the region covered by the HT peak.  

When a match between an RI and the HT data is found, the evidence of the corresponding HT-methods is added to the corresponding RI. This process is executed in each RegulonDB release. 
Program: 1.RIs_mapping_To_HT-TF-binding-datasets.py

### 2.	Analysis of the current set of RIs.
The anatomy of the current set of RIs was analyzed using the program 3.RIs_anatomy_analysis.R

### 3. To assess the contribution of HT evidence to the RIs confidence level.
To analyze the contribution of each HT-binding methodology to the confidence level of the current RI set, the following process was performed: Using the 'Confidence Level Calculator Tool' from RegulonDB, the HT-binding evidence codes were excluded to recalculate the confidence level of the TF-RISet, and the results were downloaded. Finally, the program '4.RIs_confidence_level_analysis.R' was run to count and graph RIs with confidence levels Confirmed, Strong, and Weak for each case.

### 4. HT-binding methodology efficacies in recovering sites from classical RIs in RegulonDB

To evaluate the performance of HT-binding methodologies (ChIP-seq, ChIP-exo, gSELEX, and DAP-seq) in recovering Transcription Factor Regulatory Sites (TFRSs) from RegulonDB, the RISet was filtered to exclude circularity. For each methodology, TFs were evaluated if they had at least one dataset in the subcollection of HT TF-binding and at least one RI in the filtered set from RegulonDB. The filtered RISet was mapped to the datasets from each methodology using the program: 1.RIs_mapping_To_HT-TF-binding-datasets.py. Afterwards, the total number of sites in the subset of RIs mapped and the percentage of them detected for the corresponding methodology were calculated for each TF using the program: 5.TFRSs_recovered_by_methods.py . Finally, the average percentage of sites recovered was calculated for each methodology. 
#### 5. Statistical Analysis of TFRSs recovery by HT-binding methodology
To evaluate differences in the detection performance of the methodologies we conducted a Kruskal-Wallis test, along with the Bonferroni correction, to compare mean rank differences across the four groups, considering the non-parametric nature of the data and the variability in the number of TFs analyzed in each case.
Program:  6.Statistical_analysis.R

### License

Apache v2.0


### Support contact information

regulondb@ccg.unam.mx

Paloma Lara <palomalf86@gmail.com>
