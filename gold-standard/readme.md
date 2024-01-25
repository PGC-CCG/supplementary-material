# TF RIs Architecture of Evidence Types

### *A Gold Standard for Transcription Factor Regulatory Interactions in Escherichia coli K-12: Architecture of Evidence Types*

Here, we present a detailed  analysis of the sources of knowledge supporting the collection of transcriptional regulatory interactions (RIs) of *E. coli K-12*. An RI groups the transcription factor, its effect (positive or negative)  and the regulated  target, a promoter, a gene or transcription unit. 

We improved the evidence codes so that  specific methods are incorporated , and  classified  into independent groups. On this basis we  updated the computation of confidence levels, weak, strong, or confirmed, for the collection of RIs. 

This process enriched the evidence of close to one quarter of RIs in RegulonDB release 11.1. Based on the new computational capabilities of our improved annotation of evidence sources, we can now analyze the internal architecture of evidence, their categories (experimental, classical, HT, computational), and confidence levels. 

## Analysis of the set of RIs

#### requirements

The analyses of the anatomy of RI knowledge presented here were performed using 

- R (2022.06.23, version 4.2.1), 
- Rstudio (2022.07.1, Build 554), and the ggplot2 (version 3.4.0) library
- Python release 3.11 



All scripts and computational processes built to generate the data and analyses presented in this analysis are:
 
1. Run_Coordinate-Updates.py
2. 1.RIs_mapping_To_HT-TF-binding-datasets.py3. 2.New_HT-evidence_for_RIs.py4. 3.RIs_anatomy_analysis.R5. 4.RIs_confidence_level_analysis.R6. 5.RIs_recovered_by_methods.py


### Mapping collection of TFBSs-HT to TFRSs from RegulonDB.

The collection of HT TFBSs contains four subcollections with different number of TFs: DAP-seq, ChIP-seq, ChIP-exo, and gSELEX. The mapping was made to the TFRSs sites in RegulonDB.

In order to make these collections comparable among them and with RegulonDB TFRSs, multiple steps were implemented that together constituted what we call “mapping,” of HT-binding data with known sites. This mapping involves: 

#### 1. Uniformization of the genome coordinates for all datasets. 

The coordinates of the DAP-seq datasets were published using the last genome version of the E. coli str. K-12 substr. MG1655 (U00096.3), so they were not modified. The ChIP-seq, gSELEX, and ChIP-exo datasets with coordinates in the past genome version (U00096.2) were updated to version U00096.3. 

Program: Run_Coordinate-Updates.py


#### 2. To map the RegulonDB RI set with peaks from the HT-TFBSs subcollections.

A program in Python was implemented that compared each RI binding site with each peak corresponding to the same TF.  A match is assumed when the RI site coordinate is within the region covered by the HT peak.  

When a match between an RI and the HT data is found, the evidence of the corresponding HT-methods is added to the corresponding RI. This process is executed in each RegulonDB release. Scripts are found in the github as mentioned.

Program: 1.RIs_mapping_To_HT-TF-binding-datasets.py

#### HT-binding methodology efficacies in recovering sites from classical RIs in RegulonDB

For the comparison of ChIP-seq, ChIP-exo, gSELEX, and DAP-seq, the RIs set was mapped to the complete collection as described before. The fraction of RIs with at least one piece of classical evidence that were recovered by each method for each TF was then calculated. TFs in each collection with zero RIs featuring at least one classical evidence were excluded from this analysis. The same algorithm was applied to determine the proportion of RIs with confirmed confidence levels without considering HT evidence in the calculation.

To evaluate differences in the detection performance of the methodologies  we conducted a Kruskal-Wallis test, along with the Bonferroni correction, to compare mean rank differences across the four groups, considering the non-parametric nature of the data and the variability in the number of TFs analyzed in each case.  

Program: 5.RIs_recovered_by_methods.py


### License

Apache v2.0


### Support contact information

regulondb@ccg.unam.mx

Paloma Lara <palomalf86@gmail.com>
