#NAME: Statistical analysis of differences between the HT methods to recover
#TFRSs from RegulonDB

#AUTHOR: Paloma Lara <palomalf86@gmail.com>

#DESCRIPTION: 
#This program allows to perform a Kruskal-Wallis test, along with the Bonferroni correction, to compare mean rank differences across the four groups.

#INPUT:file.xlsx with four columns "ChIP-exo", "ChIP-seq", "gSELEX" and "DAP-seq"
 
##SOFTWARE REQUIREMENTS##
#install.packages("tidyverse")
#install.packages("readx")

library(tidyverse)
library(readxl)

# Read data from Excel files
ChIP_exo <- read_excel("/Classical_Confirmed_TFRSs_Recovered_200.xlsx", col_names = TRUE)[[1]]
ChIP_seq <- read_excel("/Classical_Confirmed_TFRSs_Recovered_200.xlsx", col_names = TRUE)[[2]]
gSELEX <- read_excel("/Classical_Confirmed_TFRSs_Recovered_200.xlsx", col_names = TRUE)[[3]]
DAP_seq <- read_excel("/Classical_Confirmed_TFRSs_Recovered_200.xlsx", col_names = TRUE)[[4]]

# Create a data frame
data <- data.frame(
  Group = rep(c("ChIP_exo", "ChIP_seq", "gSELEX", "DAP_seq"), 
              c(length(ChIP_exo), length(ChIP_seq), length(gSELEX), length(DAP_seq))),
  Value = c(ChIP_exo, ChIP_seq, gSELEX, DAP_seq)
)

# Perform the Kruskal-Wallis test
kw_result <- kruskal.test(Value ~ Group, data = data)

# Print the result
print(kw_result)

# Perform multiple comparison tests with p-value adjustment (e.g., Bonferroni method)
comparisons <- pairwise.wilcox.test(data$Value, data$Group, p.adjust.method = "bonferroni")

# Print the comparisons
print(comparisons)