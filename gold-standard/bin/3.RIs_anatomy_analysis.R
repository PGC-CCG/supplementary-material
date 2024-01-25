# NAME: Regulatory Interaction anatomy analysis

# AUTHOR: Paloma Lara <palomalf86@gmail.com>

# DESCRIPTION: 
# This program allows the analysis of the TF RIs in terms of types, 
# confidence level, categories, and evidence types supporting them.

# INPUT: TF-RISet.txt download from https://regulondb.ccg.unam.mx/datasets

## SOFTWARE REQUIREMENTS ##
#install.packages("dplyr")
#install.packages("stringr")
#install.packages("UpSetR")
#install.packages("ggplot2")
#install.packages("data.table")

library(dplyr)
library(stringr)
library(UpSetR)
library(ggplot2)
library(grid)

##########################################################################################
## Reading and Preparing the data 
##########################################################################################
# Getting the data from the RIs file
df_RIs_set_01 = read.delim("data-input/TF-RISet_12.1.txt", comment.char="#", header = TRUE, sep = "\t", fill = TRUE)

# Filtering DksA RIs because it is not a TF.
df_RIs_set <- df_RIs_set_01 %>% filter(X4.regulatorName != "DksA")
View(df_RIs_set)

# The RIs with confidence level unknown can be considered weak
df_RIs_set$"X20.confidenceLevel" <- str_replace_all(df_RIs_set$"X20.confidenceLevel", fixed("?"), "W")

# Joining the TFBS and RI evidences in one column
df_RIs_set$"allEvidence" <- paste(df_RIs_set$X21.tfrsEvidence, df_RIs_set$X22.riEvidence, sep = ";")
df_RIs_set$"allEvidence" <- sub(";$", "", df_RIs_set$"allEvidence")
df_RIs_set$"allEvidence" <- sub("^;", "", df_RIs_set$"allEvidence")
df_RIs_set$"allEvidence" <- sapply(strsplit(df_RIs_set$"allEvidence", ';'), function(i)paste(unique(i), collapse = ';'))
df_RIs_set$"allEvidence" <- sapply(strsplit(df_RIs_set$"allEvidence", ';'), function(i)paste(sort(i), collapse = ';'))

# Create the Evidence catalog for RIs - Create a list with all evidences for all RIs
indEvsAllRiAndSite<- df_RIs_set %>%
  select(allEvidence) %>%
  cSplit("allEvidence", sep=";", direction = "long") %>%
  count(allEvidence)

# Create a new column with all evidences for each RI, but with similar binding-evidence types grouped
df_RIs_set$"riEvGrouped" <- df_RIs_set$"allEvidence"
df_RIs_set$"riEvGrouped" <- str_replace_all(df_RIs_set$"riEvGrouped", "EXP-IEP-GENE-EXPRESSION-ANALYSIS", "Expression")
df_RIs_set$"riEvGrouped" <- str_replace_all(df_RIs_set$"riEvGrouped", "EXP-IEP-RNA-SEQ", "Expression")
df_RIs_set$"riEvGrouped" <- str_replace_all(df_RIs_set$"riEvGrouped", "EXP-IEP-MICROARRAY", "Expression")
df_RIs_set$"riEvGrouped" <- str_replace_all(df_RIs_set$"riEvGrouped", "EXP-IEP-BETA-GAL", "Expression")
df_RIs_set$"riEvGrouped" <- str_replace_all(df_RIs_set$"riEvGrouped", "EXP-IEP-LUCIFERASE", "Expression")
df_RIs_set$"riEvGrouped" <- str_replace_all(df_RIs_set$"riEvGrouped", "EXP-IEP-NORTHERN", "Expression")
df_RIs_set$"riEvGrouped" <- str_replace_all(df_RIs_set$"riEvGrouped", "EXP-IEP-QRTPCR", "Expression")
df_RIs_set$"riEvGrouped" <- str_replace_all(df_RIs_set$"riEvGrouped", "EXP-IEP-RTPCR", "Expression")
df_RIs_set$"riEvGrouped" <- str_replace_all(df_RIs_set$"riEvGrouped", "EXP-IEP-PRIMER-EXTENSION-FOR-EXPRESSION", "Expression")
df_RIs_set$"riEvGrouped" <- str_replace_all(df_RIs_set$"riEvGrouped", "EXP-IEP", "Expression")
df_RIs_set$"riEvGrouped" <- str_replace_all(df_RIs_set$"riEvGrouped", "EXP-IMP-SITE-MUTATION", "Site mutation")
df_RIs_set$"riEvGrouped" <- str_replace_all(df_RIs_set$"riEvGrouped", "EXP-IDA-BINDING-OF-PURIFIED-PROTEINS-EMSA", "Binding of purified proteins")
df_RIs_set$"riEvGrouped" <- str_replace_all(df_RIs_set$"riEvGrouped", "EXP-IDA-BINDING-OF-PURIFIED-PROTEINS", "Binding of purified proteins")
df_RIs_set$"riEvGrouped" <- str_replace_all(df_RIs_set$"riEvGrouped", "EXP-CHIP-SEQ-MANUAL", "ChIP-seq")
df_RIs_set$"riEvGrouped" <- str_replace_all(df_RIs_set$"riEvGrouped", "EXP-CHIP-SEQ", "ChIP-seq")
df_RIs_set$"riEvGrouped" <- str_replace_all(df_RIs_set$"riEvGrouped", "EXP-CHIP-CHIP-MANUAL", "ChIP-chip")
df_RIs_set$"riEvGrouped" <- str_replace_all(df_RIs_set$"riEvGrouped", "EXP-CHIP-CHIP", "ChIP-chip")
df_RIs_set$"riEvGrouped" <- str_replace_all(df_RIs_set$"riEvGrouped", "EXP-CHIP-EXO-MANUAL", "ChIP-exo")
df_RIs_set$"riEvGrouped" <- str_replace_all(df_RIs_set$"riEvGrouped", "EXP-CHIP-EXO", "ChIP-exo")
df_RIs_set$"riEvGrouped" <- str_replace_all(df_RIs_set$"riEvGrouped", "EXP-CHIP-PCR-MANUAL", "ChIP-PCR")
df_RIs_set$"riEvGrouped" <- str_replace_all(df_RIs_set$"riEvGrouped", "EXP-CHIP-PCR", "ChIP-PCR")
df_RIs_set$"riEvGrouped" <- str_replace_all(df_RIs_set$"riEvGrouped", "EXP-GSELEX", "genomic SELEX")
df_RIs_set$"riEvGrouped" <- str_replace_all(df_RIs_set$"riEvGrouped", "EXP-IDA-BINDING-OF-CELLULAR-EXTRACTS-EMSA", "Binding of cellular extracts")
df_RIs_set$"riEvGrouped" <- str_replace_all(df_RIs_set$"riEvGrouped", "EXP-IDA-BINDING-OF-CELLULAR-EXTRACTS", "Binding of cellular extracts")
df_RIs_set$"riEvGrouped" <- str_replace_all(df_RIs_set$"riEvGrouped", "HTP-HDA-DAP-SEQ", "DAP-seq")
df_RIs_set$"riEvGrouped" <- str_replace_all(df_RIs_set$"riEvGrouped", "COMP-HINF-SIMILAR-TO-CONSENSUS", "Computational analysis")
df_RIs_set$"riEvGrouped" <- str_replace_all(df_RIs_set$"riEvGrouped", "COMP-AINF-SIMILAR-TO-CONSENSUS", "Computational analysis")
df_RIs_set$"riEvGrouped" <- str_replace_all(df_RIs_set$"riEvGrouped", "COMP-AINF-PATTERN-DISCOVERY", "Computational analysis")
df_RIs_set$"riEvGrouped" <- str_replace_all(df_RIs_set$"riEvGrouped", "COMP-HINF-PATTERN-DISCOVERY", "Computational analysis")
df_RIs_set$"riEvGrouped" <- str_replace_all(df_RIs_set$"riEvGrouped", "EXP-IMP-REACTION-BLOCKED", "Reaction blocked in mutants")
df_RIs_set$"riEvGrouped" <- str_replace_all(df_RIs_set$"riEvGrouped", "EXP-IDA-PURIFIED-PROTEIN:W", "Binding of purified proteins:S")
df_RIs_set$"riEvGrouped" <- str_replace_all(df_RIs_set$"riEvGrouped", "COMP-HINF", "Computational analysis")
df_RIs_set$"riEvGrouped" <- str_replace_all(df_RIs_set$"riEvGrouped", "COMP-AINF", "Computational analysis")
df_RIs_set$"riEvGrouped" <- str_replace_all(df_RIs_set$"riEvGrouped", "COMP-IBA", "Computational analysis")
df_RIs_set$"riEvGrouped" <- str_replace_all(df_RIs_set$"riEvGrouped", "COMP", "Computational analysis")
df_RIs_set$"riEvGrouped" <- str_replace_all(df_RIs_set$"riEvGrouped", "IC", "Inferred by curator")
df_RIs_set$"riEvGrouped" <- str_replace_all(df_RIs_set$"riEvGrouped", "EXP-IMP", "Expression")
df_RIs_set$"riEvGrouped" <- str_replace_all(df_RIs_set$"riEvGrouped", "EXP-IPI", "Inferred from physical interaction")
df_RIs_set$"riEvGrouped" <- str_replace_all(df_RIs_set$"riEvGrouped", "EXP-TAS", "Author statement")
df_RIs_set$"riEvGrouped" <- str_replace_all(df_RIs_set$"riEvGrouped", "EXP-IGI", "Inferred from genetic interaction")
df_RIs_set$"riEvGrouped" <- str_replace_all(df_RIs_set$"riEvGrouped", "AS-NAS", "Author statement")
df_RIs_set$"riEvGrouped" <- str_replace_all(df_RIs_set$"riEvGrouped", "AS-TAS", "Author statement")
df_RIs_set$"riEvGrouped" <- str_replace_all(df_RIs_set$"riEvGrouped", "AS", "Author statement")
df_RIs_set$"riEvGrouped" <- str_replace_all(df_RIs_set$"riEvGrouped", "EXP-IDA", "Inferred from direct assay")
df_RIs_set$"riEvGrouped" <- sapply(strsplit(df_RIs_set$"riEvGrouped", ';'), function(i)paste(unique(i), collapse = ';'))
df_RIs_set$"riEvGrouped" <- sapply(strsplit(df_RIs_set$"riEvGrouped", ';'), function(i)paste(sort(i), collapse = ';'))

## Create a new column with only binding evidence types grouped
df_RIs_set$"bindingEvGrouped"<- df_RIs_set$"riEvGrouped" 
df_RIs_set$"bindingEvGrouped"<- str_replace_all(df_RIs_set$"bindingEvGrouped",fixed("Expression:W"),"-")
df_RIs_set$"bindingEvGrouped" <- sapply(strsplit(df_RIs_set$"bindingEvGrouped", ';'), function(i)paste(unique(i), collapse = ';'))
df_RIs_set$"bindingEvGrouped" <- sapply(strsplit(df_RIs_set$"bindingEvGrouped", ';'), function(i)paste(sort(i), collapse = ';'))
df_RIs_set$"bindingEvGrouped"<- str_replace_all(df_RIs_set$"bindingEvGrouped", "-;","")

# Create a new column with only binding categories
df_RIs_set$"bindingEvCategory"<- df_RIs_set$"X25.riEvCategory"
df_RIs_set$"bindingEvCategory"<- str_replace_all(df_RIs_set$"bindingEvCategory", fixed("|"), (","))
df_RIs_set$"bindingEvCategory" <- sapply(strsplit(df_RIs_set$"bindingEvCategory", ','), function(i)paste(unique(i), collapse = ','))
df_RIs_set$"bindingEvCategory" <- sapply(strsplit(df_RIs_set$"bindingEvCategory", ','), function(i)paste(sort(i), collapse = ','))
df_RIs_set$"bindingEvCategory"<- str_replace_all(df_RIs_set$"bindingEvCategory", fixed(" ,"), fixed(","))
df_RIs_set$"bindingEvCategory"<- str_replace_all(df_RIs_set$"bindingEvCategory", fixed(", "), fixed(","))
df_RIs_set$"bindingEvCategory"<- str_replace_all(df_RIs_set$"bindingEvCategory", fixed("non-experimental,"), "")
df_RIs_set$"bindingEvCategory"<- str_replace_all(df_RIs_set$"bindingEvCategory", fixed("High-throughput expression,"), "")
df_RIs_set$"bindingEvCategory"<- str_replace_all(df_RIs_set$"bindingEvCategory", fixed("Classical expression,"), "")
df_RIs_set$"bindingEvCategory"<- str_replace_all(df_RIs_set$"bindingEvCategory", fixed("independent cross-validation,"), "")
df_RIs_set$"bindingEvCategory"<- str_replace_all(df_RIs_set$"bindingEvCategory", fixed(",non-experimental"), fixed(""))
df_RIs_set$"bindingEvCategory"<- str_replace_all(df_RIs_set$"bindingEvCategory", fixed(",High-throughput expression"), "")
df_RIs_set$"bindingEvCategory"<- str_replace_all(df_RIs_set$"bindingEvCategory", fixed(",Classical expression"), "")
df_RIs_set$"bindingEvCategory"<- str_replace_all(df_RIs_set$"bindingEvCategory", "non-experimental", "")
df_RIs_set$"bindingEvCategory"<- str_replace_all(df_RIs_set$"bindingEvCategory", fixed(",independent cross-validation"), "")
df_RIs_set$"bindingEvCategory"<- str_replace_all(df_RIs_set$"bindingEvCategory", "High-throughput expression", "")
df_RIs_set$"bindingEvCategory"<- str_replace_all(df_RIs_set$"bindingEvCategory", "Classical expression", "")
df_RIs_set$"bindingEvCategory"<- str_replace_all(df_RIs_set$"bindingEvCategory", "Classical experiment", "")
df_RIs_set$"bindingEvCategory"<- str_replace_all(df_RIs_set$"bindingEvCategory", "independent cross-validation", "")
df_RIs_set$"bindingEvCategory"<- str_replace_all(df_RIs_set$"bindingEvCategory", (" "), (""))
df_RIs_set$"bindingEvCategory" <- sub(",$", "", df_RIs_set$"bindingEvCategory")

#Create a new column with only binding categories summarized
df_RIs_set$"bindingCategorySummary"<-"nonexperimental"
df_RIs_set$"bindingCategorySummary"[df_RIs_set$"bindingEvCategory"=="Classicalbinding"]<-"Classical"
df_RIs_set$"bindingCategorySummary"[df_RIs_set$"bindingEvCategory"=="High-throughputbinding"]<-"HT"
df_RIs_set$"bindingCategorySummary"[df_RIs_set$"bindingEvCategory"=="Classicalbinding,High-throughputbinding"]<-"Classical & HT"


#########################################################################################
# Counts of confidence level for the three types of RIs for built the Table 1
##########################################################################################

#TF-promoter
tfPromoterConfidenceLevel<- df_RIs_set %>%
  filter(X2.riType=="tf-promoter") %>%
  select(X20.confidenceLevel) %>%
  filter(X20.confidenceLevel!="")%>%
  count(X20.confidenceLevel)
tfPromoterConfidenceLevel$riType<-"TF-promoter"

#TF-tu
tfTuConfidenceLevel<- df_RIs_set %>%
  filter(X2.riType=="tf-tu") %>%
  select(X20.confidenceLevel) %>%
  count(X20.confidenceLevel)
tfTuConfidenceLevel$riType<-"TF-TU"

#TF-gene
tfGeneConfidenceLevel<- df_RIs_set %>%
  filter(X2.riType=="tf-gene") %>%
  select(X20.confidenceLevel) %>%
  count(X20.confidenceLevel)
tfGeneConfidenceLevel$riType<-"TF-gene"


#### Table 1: Ri types, grouped by confidence level
riTypesAndConfidence<-rbind(tfPromoterConfidenceLevel,tfTuConfidenceLevel,tfGeneConfidenceLevel)
riTypesAndConfidence<-riTypesAndConfidence %>% rename ("Confidence_level"=X20.confidenceLevel)
riTypesAndConfidence<-riTypesAndConfidence[c("riType", "Confidence_level", "n")]
write.table(riTypesAndConfidence, file = "results/RIs_Evidences_Analysis_12.1/RI_types&confidence-level_RDB12.1.v3.0.txt", append = FALSE, row.names = FALSE, col.names = TRUE, sep = "\t")

### Figure 2A: Barplot of RIs types and confidence level 
Figure2A <- ggplot(riTypesAndConfidence, aes(x = factor(riType), y = n, fill = Confidence_level, colour = Confidence_level)) + 
  xlab("RI type") +
  geom_bar(position="stack", stat = "identity") +
  theme(
    axis.text.x = element_text(size = 8),
    panel.background = element_rect(fill = "white"),
    axis.line = element_line(colour = "black"),
    panel.border = element_rect(colour = "black", fill = NA, size = 1),
    legend.position = "right",  # Colocar la leyenda en el lado derecho
    legend.box = "vertical",  # Mostrar la leyenda en una disposición vertical
    legend.text = element_text(size = 8),  # Ajustar el tamaño de fuente de las etiquetas de la leyenda
    legend.title = element_text(size = 10),
    axis.title.x = element_text(size = 10),
    legend.margin = margin(0, 0, 0, -10)  # Reducir el espacio en el lado derecho de la leyenda
  )  +
  ylim(0,4100)+
  labs(y = "Number of RIs")
print(Figure2A)


################################################################################################
# Get counts of category (HT or classical) for the three Ri types (Table S1), for built the Figure 2B
#########################################################################################

#TF-promoter
tfPromoterthroughputType<- df_RIs_set %>%
  filter(X2.riType=="tf-promoter") %>%
  select(bindingCategorySummary) %>%
  count(bindingCategorySummary)
tfPromoterthroughputType$riType<-"TF-promoter"

#TF-tu
tfTuthroughputType<- df_RIs_set %>%
  filter(X2.riType=="tf-tu") %>%
  select(bindingCategorySummary) %>%
  count(bindingCategorySummary)
tfTuthroughputType$riType<-"TF-TU"

#TF-gene
tfGenetfTuthroughputType<- df_RIs_set %>%
  filter(X2.riType=="tf-gene") %>%
  select(bindingCategorySummary) %>%
  count(bindingCategorySummary)
tfGenetfTuthroughputType$riType<-"TF-gene"


### Table: Table with the counts of RI Types and confidence level
riTypesAndThroughputType<-rbind(tfPromoterthroughputType,tfTuthroughputType,tfGenetfTuthroughputType)
riTypesAndThroughputType<-riTypesAndThroughputType %>% rename ("Evidence_category"=bindingCategorySummary)
#riTypesAndThroughputType$Evidence_category<- str_replace_all(riTypesAndThroughputType$Evidence_category,"none","not experimental")
riTypesAndCategory<-riTypesAndThroughputType[c("riType", "Evidence_category", "n")]
write.table(riTypesAndThroughputType, file = "results/RIs_Evidences_Analysis_12.1/riTypes&Category_RDB12.1_RIsv3.0.txt", append = FALSE, row.names = FALSE, col.names = TRUE, sep = "\t")

### Figure 2B:
Figure2B <- ggplot(riTypesAndThroughputType, aes(x = factor(riType), y = n, fill = Evidence_category, colour = Evidence_category)) + 
  xlab("RI type") +
  geom_bar(position="stack", stat = "identity") +
  theme(
    axis.text.x = element_text(size = 8),
    panel.background = element_rect(fill = "white"),
    axis.line = element_line(colour = "black"),
    panel.border = element_rect(colour = "black", fill = NA, size = 1),
    legend.position = "right",  # Colocar la leyenda en el lado derecho
    legend.box = "vertical",  # Mostrar la leyenda en una disposición vertical
    legend.text = element_text(size = 8),  # Ajustar el tamaño de fuente de las etiquetas de la leyenda
    legend.title = element_text(size = 10),
    axis.title.x = element_text(size = 10),
    legend.margin = margin(0, 0, 0, -10)  # Reducir el espacio en el lado derecho de la leyenda
  ) +
  ylim(0,4100)+
  labs(y = "Number of RIs")
print(Figure2B)


############################################################################################
#Get the counts of RIs with the different confidence levels and grouped by category for built Figure 4
#########################################################################################

#Classical
througputCounts<-df_RIs_set %>%
  count(bindingCategorySummary)
ClassicalConfidenceLevel<- df_RIs_set %>%
  filter(bindingCategorySummary=="Classical") %>%
  select(X20.confidenceLevel) %>%
  count(X20.confidenceLevel)
ClassicalConfidenceLevel$throughput<-"Classical"

#HT
HTConfidenceLevel<- df_RIs_set %>%
  filter(bindingCategorySummary=="HT") %>%
  select(X20.confidenceLevel) %>%
  count(X20.confidenceLevel)
HTConfidenceLevel$throughput<-"HT"

#Classical HT
HTClassicalConfidenceLevel<- df_RIs_set %>%
  filter(bindingCategorySummary=="Classical & HT") %>%
  select(X20.confidenceLevel) %>%
  count(X20.confidenceLevel)
HTClassicalConfidenceLevel$throughput<-"Classical & HT"

#Not experimental
throughputnoneConfidenceLevel<- df_RIs_set %>%
  filter(bindingCategorySummary=="nonexperimental") %>%
  select(X20.confidenceLevel) %>%
  count(X20.confidenceLevel)
throughputnoneConfidenceLevel$throughput<-"nonexperimental"
throughputnoneConfidenceLevel<- throughputnoneConfidenceLevel %>%
  filter(X20.confidenceLevel!="")

# Table: able with the counts of RIs with the different confidence levels and grouped by category
throughputTypesAndConfidence<-rbind(ClassicalConfidenceLevel,HTConfidenceLevel,HTClassicalConfidenceLevel,throughputnoneConfidenceLevel)
throughputTypesAndConfidence<-throughputTypesAndConfidence %>% rename ("Confidence_level"=X20.confidenceLevel)

# Figure 2C: 
Figure2C <- ggplot(throughputTypesAndConfidence, aes(x = factor(throughput), y = n, fill = Confidence_level, colour = Confidence_level)) + 
  xlab("Evidence category") +
  geom_bar(position="stack", stat = "identity") +
  theme(
    axis.text.x = element_text(size = 8),
    panel.background = element_rect(fill = "white"),
    axis.line = element_line(colour = "black"),
    panel.border = element_rect(colour = "black", fill = NA, size = 1),
    legend.position = "right",  # Colocar la leyenda en el lado derecho
    legend.box = "vertical",  # Mostrar la leyenda en una disposición vertical
    legend.text = element_text(size = 8),  # Ajustar el tamaño de fuente de las etiquetas de la leyenda
    legend.title = element_text(size = 10),
    axis.title.x = element_text(size = 10),
    legend.margin = margin(0, 0, 0, -10),  # Reducir el espacio en el lado derecho de la leyenda
  ) +
  ylim(0,2000)+
  labs(y = "Number of RIs")
print(Figure2C)


## Figure 2 ABC: Plot
# Make a vector of tags for the Figures
etiquetas <- c("A", "B", "C")

# Make a list of tags for each panel
etiquetas_list <- lapply(etiquetas, function(etiqueta) {
  textGrob(etiqueta, x = 0.02, y = 0.5, gp = gpar(fontsize = 12, fontface = "bold"))
})

# Make the combined graph
combined_plot <- arrangeGrob(
  arrangeGrob(Figure2A, top = etiquetas_list[[1]]),
  arrangeGrob(Figure2B, top = etiquetas_list[[2]]),
  arrangeGrob(Figure2C, top = etiquetas_list[[3]]),
  ncol = 1
)

# Save the combined graph
ggsave("results/RIs_Evidences_Analysis_12.1/Figure2_A_B_C_RDB12.1_v3.0.png", combined_plot, width = 6, height = 8, units = "in", dpi = 300)


#########################################################################################
# Built an Upset of binding evidence combinations found in all RIs
#########################################################################################

combinationsBindingEvRisAbundances<- df_RIs_set %>%
  select(bindingEvGrouped) %>%
  filter(bindingEvGrouped!="-") %>%
  count(bindingEvGrouped)
combinationsBindingEvRisAbundances<- combinationsBindingEvRisAbundances[order(combinationsBindingEvRisAbundances$n,  decreasing = TRUE), ]
combinationsBindingEvRisAbundances$bindingEvGrouped <- str_replace_all (combinationsBindingEvRisAbundances$bindingEvGrouped, ";", "&")
combinationsBindingEvRisAbundancesWithCutOff <- combinationsBindingEvRisAbundances %>%
  filter(n>20)
evCombinationNames <- combinationsBindingEvRisAbundances$bindingEvGrouped 
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
      text.scale = .9, 
      point.size = .8, 
      line.size = .3)
grid.text("Binding evidence supporting current RIs",x = 0.72, y=0.95, gp=gpar(fontsize=10))

########################################################################3
# Built an Upset of binding evidence combinations found in Confirmed RIs (Figure 3A)
########################################################################3

combinationsBindingEvConfirmedRisAbundances<- df_RIs_set %>%
  filter(X20.confidenceLevel=="C") %>%
  select(bindingEvGrouped) %>%
  filter(bindingEvGrouped!="-") %>%
  count(bindingEvGrouped)
combinationsBindingEvConfirmedRisAbundances<- combinationsBindingEvConfirmedRisAbundances[order(combinationsBindingEvConfirmedRisAbundances$n,  decreasing = TRUE), ]
combinationsBindingEvConfirmedRisAbundances$bindingEvGrouped <- str_replace_all (combinationsBindingEvConfirmedRisAbundances$bindingEvGrouped, ";", "&")
combinationsBindingEvConfirmedRisAbundancesWithCutOff <- combinationsBindingEvConfirmedRisAbundances %>%
  filter(n>20)
evCombinationConfirmedNames <- combinationsBindingEvConfirmedRisAbundances$bindingEvGrouped 
evCombinationConfirmedCounts <- combinationsBindingEvConfirmedRisAbundances$n
names(evCombinationConfirmedCounts)<-evCombinationConfirmedNames
evCombinationConfirmedCounts
upset(fromExpression(evCombinationConfirmedCounts), 
      nintersects = 40, 
      nsets = 29, 
      order.by = "freq", 
      decreasing = T, 
      mb.ratio = c(0.6, 0.4),
      number.angles = 0, 
      text.scale = .9, 
      point.size = .8, 
      line.size = .3)
grid.text("Binding evidence supporting confirmed RIs",x = 0.72, y=0.95, gp=gpar(fontsize=10))

########################################################################
# Built an Upset of binding evidence combinations found in strong RIs (Figure 3B)
########################################################################

combinationsBindingEvStrongRisAbundances<- df_RIs_set %>%
  filter(X20.confidenceLevel=="S") %>%
  select(bindingEvGrouped) %>%
  filter(bindingEvGrouped!="-") %>%
  count(bindingEvGrouped)
combinationsBindingEvStrongRisAbundances<- combinationsBindingEvStrongRisAbundances[order(combinationsBindingEvStrongRisAbundances$n,  decreasing = TRUE), ]
combinationsBindingEvStrongRisAbundances$bindingEvGrouped <- str_replace_all (combinationsBindingEvStrongRisAbundances$bindingEvGrouped, ";", "&")
combinationsBindingEvStrongRisAbundancesWithCutOff <- combinationsBindingEvStrongRisAbundances %>%
  filter(n>20)
evCombinationStrongNames <- combinationsBindingEvStrongRisAbundances$bindingEvGrouped 
evCombinationStrongCounts <- combinationsBindingEvStrongRisAbundances$n
names(evCombinationStrongCounts)<-evCombinationStrongNames
evCombinationStrongCounts
upset(fromExpression(evCombinationStrongCounts), 
      nintersects = 40, 
      nsets = 29, 
      order.by = "freq", 
      decreasing = T, 
      mb.ratio = c(0.6, 0.4),
      number.angles = 0, 
      text.scale = .9, 
      point.size = .8, 
      line.size = .3)
grid.text("Binding evidence supporting strong RIs",x = 0.72, y=0.95, gp=gpar(fontsize=10))

################################################################
# Built an Upset of binding evidence combinations found in weak RIs (Figure 3C)
########################################################################
combinationsBindingEvWeakRisAbundances<- df_RIs_set %>%
  filter(X20.confidenceLevel=="W") %>%
  select(bindingEvGrouped) %>%
  filter(bindingEvGrouped!="-") %>%
  count(bindingEvGrouped)
combinationsBindingEvWeakRisAbundances<- combinationsBindingEvWeakRisAbundances[order(combinationsBindingEvWeakRisAbundances$n,  decreasing = TRUE), ]
combinationsBindingEvWeakRisAbundances$bindingEvGrouped <- str_replace_all (combinationsBindingEvWeakRisAbundances$bindingEvGrouped, ";", "&")
combinationsBindingEvWeakRisAbundancesWithCutOff <- combinationsBindingEvWeakRisAbundances %>%
  filter(n>20)
evCombinationWeakNames <- combinationsBindingEvWeakRisAbundances$bindingEvGrouped 
evCombinationWeakCounts <- combinationsBindingEvWeakRisAbundances$n
names(evCombinationWeakCounts)<-evCombinationWeakNames
evCombinationWeakCounts
upset(fromExpression(evCombinationWeakCounts), 
      nintersects = 40, 
      nsets = 29, 
      order.by = "freq", 
      decreasing = T, 
      mb.ratio = c(0.6, 0.4),
      number.angles = 0, 
      text.scale = .9, 
      point.size = .8, 
      line.size = .3)
grid.text("Binding evidence supporting weak RIs",x = 0.72, y=0.95, gp=gpar(fontsize=10))

########################################################################
##Additional analysis
########################################################################

#Counts of each type of RIs
nrow(df_RIs_set[df_RIs_set$X2.riType=="tf-gene",])
nrow(df_RIs_set[df_RIs_set$X2.riType=="tf-tu",])
nrow(df_RIs_set[df_RIs_set$X2.riType=="tf-promoter",])

#Counts of RIs with the diferent confidence levels
nrow(df_RIs_set[df_RIs_set$X20.confidenceLevel=="C",])
nrow(df_RIs_set[df_RIs_set$X20.confidenceLevel=="S",])
nrow(df_RIs_set[df_RIs_set$X20.confidenceLevel=="W",])

#Counts of binding categories
throughput_ri_abundances<- df_RIs_set %>%
  select(bindingCategorySummary) %>%
  count(bindingCategorySummary)

#Counts of RIs with HT evidence (without classical evidence) and confidence level confirmed
HTConfirmed<- df_RIs_set %>%
  filter(X20.confidenceLevel=="C") %>%
  filter(bindingCategorySummary=="HT") 

##Save in a file the table with all RI evidence types grouped, where the expression evidence types are indicated only as Expression
ind_evs_all_ri_abundances<- df_RIs_set %>%
  select(riEvGrouped) %>%
  cSplit("riEvGrouped", sep=";", direction = "long") %>%
  filter(riEvGrouped!="-") %>%
  count(riEvGrouped)
ind_evs_all_ri_abund_ord <- ind_evs_all_ri_abundances[order(ind_evs_all_ri_abundances$n,  decreasing = TRUE), ]
write.table(ind_evs_all_ri_abund_ord, file = "results/RIs_Evidences_Analysis_12.1/Evidences_from_all_RIs_12.1.v3.0.txt", append = FALSE, row.names = FALSE, col.names = TRUE, sep = "\t")


## Calculate the abundance of each binding category 
category_ri_abundances<- df_RIs_set %>%
  select(X25.riEvCategory) %>%
  cSplit("X25.riEvCategory", sep="|", direction = "long") %>%
  filter(X25.riEvCategory!="-") %>%
  count(X25.riEvCategory)
category_ri_abundances <- category_ri_abundances[order(category_ri_abundances$n,  decreasing = TRUE), ]


#Get the subset of RIs with classical evidence for binding and confidence level weak
classicalRisW<- df_RIs_set %>%
  filter(bindingCategorySummary=="Classical")%>%
  filter(X20.confidenceLevel=="W")

#Save in a file the table with all RI binding evidence types grouped
select(bindingEvGrouped) %>%
  cSplit("bindingEvGrouped", sep=";", direction = "long") %>%
  filter(bindingEvGrouped!="-") %>%
  count(bindingEvGrouped)
ind_binding_evs_all_ri_abundances <- ind_binding_evs_all_ri_abundances[order(ind_binding_evs_all_ri_abundances$n,  decreasing = TRUE), ]
write.table(ind_binding_evs_all_ri_abundances, file = "results/RIs_Evidences_Analysis_12.1/RI_binding_ev_12.1.v3.0.txt", append = FALSE, row.names = FALSE, col.names = TRUE, sep = "\t")

  