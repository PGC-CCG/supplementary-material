library(dplyr)
library(splitstackshape)
library(stringr)
df_RIs_maped = read.delim("/Volumes/GoogleDrive/Shared drives/PGC-02.Proyectos_vigentes/Curacion/Analisis_HT_nuevo_conocimiento/3.Desarrollo/Golden_standard/Mapeo_TF-gene-to-RIs/output/TF_1gene_func_mapped_v1.txt", header = TRUE, sep = "\t", fill = TRUE)
View(df_RIs_maped)
df_RIs_maped$"riTypes"<- str_replace_all(df_RIs_maped$"riTypes", " ", "")
df_RIs_maped$"riTypesUniq" <- sapply(strsplit(df_RIs_maped$"riTypes", ','), function(i)paste(unique(i), collapse = ','))
df_RIs_set$X27.tfrsEvAgrouped <- str_replace_all(df_RIs_set$X27.tfrsEvAgrouped, "-MANUAL", "")
df_RIs_maped$"riTypesUniqSort" <- sapply(strsplit(df_RIs_maped$"riTypesUniq", ','), function(i)paste(sort(i), collapse = ','))
View(df_RIs_maped)
grep(",", df_RIs_maped$"riTypesUniqSort")
#Obtener la lista de todas interacciones TF-gene-funcion que tienen mas de un tipo de RI asociada
df_RIs_redundant<- df_RIs_maped %>%
  filter(grepl(',', riTypesUniqSort))
View(df_RIs_redundant)
write.table(df_RIs_redundant, file = "/Volumes/GoogleDrive/Shared drives/PGC-02.Proyectos_vigentes/Curacion/Analisis_HT_nuevo_conocimiento/3.Desarrollo/Golden_standard/Mapeo_TF-gene-to-RIs/analysis/interaction_TF-gene-function_with_redundantRIs_v1.txt", append = FALSE, row.names = FALSE, col.names = TRUE, sep = "\t")
#Obtener los conteos de interaccione TF-gen-funcion del tipo promotor, gene, tu y sus combinaciones
ri_groups_abundances<- df_RIs_maped %>%
  select(riTypesUniqSort) %>%
  count(riTypesUniqSort)
View(ri_types_abundances)
write.table(ri_groups_abundances, file = "/Volumes/GoogleDrive/Shared drives/PGC-02.Proyectos_vigentes/Curacion/Analisis_HT_nuevo_conocimiento/3.Desarrollo/Golden_standard/Mapeo_TF-gene-to-RIs/analysis/TF-gene-function_redundance_counts_v1.txt", append = FALSE, row.names = FALSE, col.names = TRUE, sep = "\t")