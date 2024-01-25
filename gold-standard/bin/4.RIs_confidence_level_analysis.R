# NAME: RIs Confidence Level Analysis

# AUTHOR: Paloma Lara <palomalf86@gmail.com>

# DESCRIPTION: 
# This program allows the analysis of the confidence level of RIs when it has
# been calculated ingnoring one or all HT-binding evidence types for create the Figure 4

# INPUT: seven files of TF-RISet.txt whith the confidence level calculated with 
# taking in account all evidence types and ingnoring one or all HT-binding evidence types
# using the “Confidence Level Calculator Tool” from RegulonDB.

## SOFTWARE REQUIREMENTS ##
# install.packages("dplyr")
# install.packages("stringr")
# install.packages("ggplot2")
# install.packages("data.table")

library(dplyr)
library(ggplot2)
library(stringr)

# List of file names
files <- c(
  "TF-RISet_12.1.txt",
  "TF-RISet_12.1_CV_without_HT.txt",
  "TF-RISet_12.1_CV_without_CHIP-CHIP.txt",
  "TF-RISet_12.1_CV_without_CHIP-SEQ.txt",
  "TF-RISet_12.1_CV_without_CHIP-EXO.txt",
  "TF-RISet_12.1_CV_without_GSELEX.txt",
  "TF-RISet_12.1_CV_without_DAP-SEQ.txt"
)

# Loop to process each file
for (file in files) {
  # Read the file
  df <- read.delim(paste0("results/RIs_Evidences_Analysis_12.1/", file),
                   comment.char = "#", header = TRUE, sep = "\t", fill = TRUE)

  # Clean white spaces
  df[] <- lapply(df, function(x) ifelse(x == "" | x == "?", "W", trimws(x)))
  df<- subset(df, !grepl("DksA", "X4.regulatorName"))
  # Save changes in new files
  write.table(df, file = paste0("results/RIs_Evidences_Analysis_12.1/modify/", file), sep = "\t", quote = FALSE, row.names = FALSE)
}

# Create a list to store the results of each file
results_list <- list()

# Loop to process each file after changes
for (file in files) {
  # Read the modified file
  df <- read.delim(paste0("results/RIs_Evidences_Analysis_12.1/modify/", file),
                   comment.char = "#", header = TRUE, sep = "\t", fill = TRUE)
  
  # Create a summary by confidence level
  summary <- df %>%
    select(X20.confidenceLevel) %>%
    count(X20.confidenceLevel)
  
  # Add the condition
  summary$condition <- paste0("With HT Evidence - ", basename(file))  # Use the file name as label
  
  # Store the result in the list
  results_list[[length(results_list) + 1]] <- summary
}

# Combine all results into a single dataframe
confLevelWithAll <- do.call(rbind, results_list)

# Change the order of the bars
confLevelWithAll$condition <- factor(confLevelWithAll$condition, levels = c("Without HT Evidence", unique(confLevelWithAll$condition)))
confLevelWithAll$condition <- str_replace_all(confLevelWithAll$condition, "With HT Evidence - TF-RISet_12.1.txt", "With HT Ev")
confLevelWithAll$condition <- str_replace_all(confLevelWithAll$condition, "With HT Evidence - TF-RISet_12.1_CV_without_HT.txt", "Without HT Ev")
confLevelWithAll$condition <- str_replace_all(confLevelWithAll$condition, "With HT Evidence - TF-RISet_12.1_CV_without_CHIP-CHIP.txt", "Without ChIP-CHIP Ev")
confLevelWithAll$condition <- str_replace_all(confLevelWithAll$condition, "With HT Evidence - TF-RISet_12.1_CV_without_CHIP-SEQ.txt", "Without ChIP-Seq Ev")
confLevelWithAll$condition <- str_replace_all(confLevelWithAll$condition, "With HT Evidence - TF-RISet_12.1_CV_without_CHIP-EXO.txt", "Without ChIP-Exo Ev")
confLevelWithAll$condition <- str_replace_all(confLevelWithAll$condition, "With HT Evidence - TF-RISet_12.1_CV_without_GSELEX.txt", "Without gSELEX Ev")
confLevelWithAll$condition <- str_replace_all(confLevelWithAll$condition, "With HT Evidence - TF-RISet_12.1_CV_without_DAP-SEQ.txt", "Without DAP-Seq Ev")

confLevelWithAll <- confLevelWithAll %>% rename(`Confidence Level` = X20.confidenceLevel)

# Create the bar chart
write.table(confLevelWithAll, file = "results/RIs_Evidences_Analysis_12.1/Table_for_Figure4.txt", row.names = FALSE, col.names = TRUE, sep = "\t") 
#Plot the Figure 4
Figures <- ggplot(confLevelWithAll, aes(x = factor(condition), y = n, fill = `Confidence Level`, colour = `Confidence Level`)) + 
  xlab("RIs set") +
  geom_bar(position = "stack", stat = "identity") +
  theme(
    axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1, size = 8),
    panel.background = element_rect(fill = "white"),
    axis.line = element_line(colour = "black"),
    panel.border = element_rect(colour = "black", fill = NA, size = 1),
    legend.position = "right",
    legend.box = "vertical",
    legend.text = element_text(size = 8),
    legend.title = element_text(size = 10),
    axis.title.x = element_text(size = 10),
    legend.margin = margin(0, 0, 0, -10)
  ) +
  ylim(0, 5800)

print(Figures)
