##NAME NetworkTF-gene_confidence_level_analysis

##VERSION: 1.0

##AUTHOR: Paloma Lara <palomalf86@gmail.com>

##DESCRIPTION: This script allow the analysis of evidence types combinations from RIs 
##CATEGORY: Data analysis

##USAGE: program [OPTIONS]

##ARGUMENTS

##SOFTWARE REQUERIMENTS

##IMPUT: The file RISet.txt, it can be download from

##https://regulondb.ccg.unam.mx/menu/download/datasets/index.jsp


##OUTPUT: A upset plot of evidence types combinations found in RIs 

##UPDATE: 24/02/2023

##LOCATION EN GIT: https://github.com/PGC-CCG/supplementary-material/tree/master/golden-standard

library(dplyr)
library(dslabs)
library(splitstackshape)
library(stringr)
library(UpSetR)
library(grid)
df_RIs_set = read.delim("../input/RISet.txt", skip=54, header = TRUE, sep = "\t", fill = TRUE)
View(df_RIs_set)
df_RIs_set$"X24.allEvidences" <- paste(df_RIs_set$ X20.tfrsEvidence, df_RIs_set $ X21.riEvidence, sep = ",")

df_RIs_set$"X24.allEvidences" <- str_replace_all(df_RIs_set$"X24.allEvidences", "-,", "")
df_RIs_set$"X25.allEvidencesUniqSort" <- sapply(strsplit(df_RIs_set$X24.allEvidences, ','), function(i)paste(unique(i), collapse = ','))
df_RIs_set$"X25.allEvidencesUniqSort" <- sapply(strsplit(df_RIs_set$"X25.allEvidencesUniqSort", ','), function(i)paste(sort(i), collapse = ','))
df_RIs_set$"X25.allEvidencesUniqSort" <- str_replace_all(df_RIs_set$"X25.allEvidencesUniqSort", "-,", "")

#Create a new column with all evidences of each RI, but with similar evidences grouped by common name 
df_RIs_set$X26.riEvAgrouped <- df_RIs_set$"X25.allEvidencesUniqSort"
df_RIs_set$X26.riEvAgrouped <- str_replace_all(df_RIs_set$X26.riEvAgrouped, "-,", "")
df_RIs_set$X26.riEvAgrouped <- str_replace_all(df_RIs_set$X26.riEvAgrouped, "EXP-IMP-SITE-MUTATION", "Site mutation")
df_RIs_set$X26.riEvAgrouped <- str_replace_all(df_RIs_set$X26.riEvAgrouped, "EXP-IDA-BINDING-OF-PURIFIED-PROTEINS", "Binding of purified proteins")
df_RIs_set$X26.riEvAgrouped <- str_replace_all(df_RIs_set$X26.riEvAgrouped, "EXP-IEP-GENE-EXPRESSION-ANALYSIS", "Gene expression analysis")
df_RIs_set$X26.riEvAgrouped <- str_replace_all(df_RIs_set$X26.riEvAgrouped, "EXP-IEP-RNA-SEQ", "RNA-seq")
df_RIs_set$X26.riEvAgrouped <- str_replace_all(df_RIs_set$X26.riEvAgrouped, "EXP-IEP-MICROARRAY", "Expression microarray")
df_RIs_set$X26.riEvAgrouped <- str_replace_all(df_RIs_set$X26.riEvAgrouped, "EXP-IEP", "Inferred from expression pattern")
df_RIs_set$X26.riEvAgrouped <- str_replace_all(df_RIs_set$X26.riEvAgrouped, "EXP-CHIP-SEQ-MANUAL", "ChIP-seq")
df_RIs_set$X26.riEvAgrouped <- str_replace_all(df_RIs_set$X26.riEvAgrouped, "EXP-CHIP-SEQ", "ChIP-seq")
df_RIs_set$X26.riEvAgrouped <- str_replace_all(df_RIs_set$X26.riEvAgrouped, "EXP-CHIP-CHIP-MANUAL", "ChIP-chip")
df_RIs_set$X26.riEvAgrouped <- str_replace_all(df_RIs_set$X26.riEvAgrouped, "EXP-CHIP-CHIP", "ChIP-chip")
df_RIs_set$X26.riEvAgrouped <- str_replace_all(df_RIs_set$X26.riEvAgrouped, "EXP-CHIP-EXO-MANUAL", "ChIP-exo")
df_RIs_set$X26.riEvAgrouped <- str_replace_all(df_RIs_set$X26.riEvAgrouped, "EXP-CHIP-EXO", "ChIP-exo")
df_RIs_set$X26.riEvAgrouped <- str_replace_all(df_RIs_set$X26.riEvAgrouped, "EXP-CHIP-PCR-MANUAL", "ChIP-PCR")
df_RIs_set$X26.riEvAgrouped <- str_replace_all(df_RIs_set$X26.riEvAgrouped, "EXP-GSELEX", "genomic SELEX")

df_RIs_set$X26.riEvAgrouped <- str_replace_all(df_RIs_set$X26.riEvAgrouped, "EXP-IDA-BINDING-OF-CELLULAR-EXTRACTS", "Binding of cellular extracts")
df_RIs_set$X26.riEvAgrouped <- str_replace_all(df_RIs_set$X26.riEvAgrouped, "EXP-CHIP-EXO", "ChIP-exo")
df_RIs_set$X26.riEvAgrouped <- str_replace_all(df_RIs_set$X26.riEvAgrouped, "COMP-HINF-SIMILAR-TO-CONSENSUS", "Computational analysis")
df_RIs_set$X26.riEvAgrouped <- str_replace_all(df_RIs_set$X26.riEvAgrouped, "COMP-AINF-SIMILAR-TO-CONSENSUS", "Computational analysis")
df_RIs_set$X26.riEvAgrouped <- str_replace_all(df_RIs_set$X26.riEvAgrouped, "COMP-AINF-PATTERN-DISCOVERY", "Computational analysis")
df_RIs_set$X26.riEvAgrouped <- str_replace_all(df_RIs_set$X26.riEvAgrouped, "COMP-HINF-PATTERN-DISCOVERY", "Computational analysis")
df_RIs_set$X26.riEvAgrouped <- str_replace_all(df_RIs_set$X26.riEvAgrouped, "EXP-IMP-REACTION-BLOCKED", "Reaction blocked in mutants")
df_RIs_set$X26.riEvAgrouped <- str_replace_all(df_RIs_set$X26.riEvAgrouped, fixed("[EXP-IDA-PURIFIED-PROTEIN|W]"), fixed("[Binding of purified proteins|S]"))
df_RIs_set$X26.riEvAgrouped <- str_replace_all(df_RIs_set$X26.riEvAgrouped, "COMP-HINF", "Computational analysis")
df_RIs_set$X26.riEvAgrouped <- str_replace_all(df_RIs_set$X26.riEvAgrouped, "COMP-AINF", "Computational analysis")
df_RIs_set$X26.riEvAgrouped <- str_replace_all(df_RIs_set$X26.riEvAgrouped, "COMP-IBA", "Computational analysis")
df_RIs_set$X26.riEvAgrouped <- str_replace_all(df_RIs_set$X26.riEvAgrouped, "COMP", "Computational analysis")

df_RIs_set$X26.riEvAgrouped <- str_replace_all(df_RIs_set$X26.riEvAgrouped, "IC", "Inferred by curator")
df_RIs_set$X26.riEvAgrouped <- str_replace_all(df_RIs_set$X26.riEvAgrouped, "EXP-IMP", "Inferred from mutant phenotype")
df_RIs_set$X26.riEvAgrouped <- str_replace_all(df_RIs_set$X26.riEvAgrouped, "EXP-TAS", "Author statement")
df_RIs_set$X26.riEvAgrouped <- str_replace_all(df_RIs_set$X26.riEvAgrouped, "EXP-IGI", "Inferred from genetic interaction")
df_RIs_set$X26.riEvAgrouped <- str_replace_all(df_RIs_set$X26.riEvAgrouped, "AS-NAS", "Author statement")
df_RIs_set$X26.riEvAgrouped <- str_replace_all(df_RIs_set$X26.riEvAgrouped, "AS-TAS", "Author statement")
df_RIs_set$X26.riEvAgrouped <- str_replace_all(df_RIs_set$X26.riEvAgrouped, "AS", "Author statement")
df_RIs_set$X26.riEvAgrouped <- str_replace_all(df_RIs_set$X26.riEvAgrouped, "EXP-IDA", "Inferred from direct assay")
df_RIs_set$"X26.riEvAgrouped" <- sapply(strsplit(df_RIs_set$X26.riEvAgrouped, ','), function(i)paste(unique(i), collapse = ','))
df_RIs_set$"X26.riEvAgrouped" <- sapply(strsplit(df_RIs_set$X26.riEvAgrouped, ','), function(i)paste(sort(i), collapse = ','))

##Create the column 27 with only binding evidence types
df_RIs_set$X27.tfrsEv<- df_RIs_set$"X26.riEvAgrouped" 
df_RIs_set$X27.tfrsEv<- str_replace_all(df_RIs_set$X27.tfrsEv,fixed("[Gene expression analysis|W]"),"-")
df_RIs_set$X27.tfrsEv<- str_replace_all(df_RIs_set$X27.tfrsEv,fixed("[RNA-seq|W]"),"-")
df_RIs_set$X27.tfrsEv<- str_replace_all(df_RIs_set$X27.tfrsEv,fixed("[Expression microarray|W]"),"-")
df_RIs_set$X27.tfrsEv<- str_replace_all(df_RIs_set$X27.tfrsEv,fixed("[Inferred from expression pattern|W]"),"-")
df_RIs_set$X27.tfrsEv <- sapply(strsplit(df_RIs_set$X27.tfrsEv, ','), function(i)paste(unique(i), collapse = ','))
df_RIs_set$X27.tfrsEv <- sapply(strsplit(df_RIs_set$X27.tfrsEv, ','), function(i)paste(sort(i), collapse = ','))
df_RIs_set$X27.tfrsEv<- str_replace_all(df_RIs_set$X27.tfrsEv, "-,","")
# Built an Upset of binding evidence combinations found in all RIs Figure 5
combinationsBindingEvRisAbundances<- df_RIs_set %>%
  select(X27.tfrsEv) %>%
  filter(X27.tfrsEv!="-") %>%
  count(X27.tfrsEv)
combinationsBindingEvRisAbundances<- combinationsBindingEvRisAbundances[order(combinationsBindingEvRisAbundances$n,  decreasing = TRUE), ]
combinationsBindingEvRisAbundances$X27.tfrsEv <- str_replace_all (combinationsBindingEvRisAbundances$X27.tfrsEv, ",", "&")
combinationsBindingEvRisAbundancesWithCutOff <- combinationsBindingEvRisAbundances %>%
  filter(n>20)
evCombinationNames <- combinationsBindingEvRisAbundances$X27.tfrsEv 
evCombinationCounts <- combinationsBindingEvRisAbundances$n
names(evCombinationCounts)<-evCombinationNames
evCombinationCounts
upset(fromExpression(evCombinationCounts), 
      nintersects = 40, 
      nsets = 29, 
      order.by = "freq", 
      decreasing = T, 
      mb.ratio = c(0.6, 0.4),
      number.angles = 0, 
      text.scale = .6, 
      point.size = .6, 
      line.size = .3)
grid.text("Binding evidence supporting current RIs",x = 0.65, y=0.95, gp=gpar(fontsize=10))