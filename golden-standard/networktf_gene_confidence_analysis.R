##NAME NetworkTF-gene_confidence_level_analysis

##VERSION: 1.0

##AUTHOR: Paloma Lara <palomalf86@gmail.com>

##DESCRIPTION: This script allow plot the number of interactions TF-gene with each condifence level

##CATEGORY: Data analysis

##USAGE: program [OPTIONS]

##ARGUMENTS

##SOFTWARE REQUERIMENTS

##IMPUT: The file NetWorkTFGene.txt, it can be download from
     
##https://regulondb.ccg.unam.mx/menu/download/datasets/index.jsp
     

##OUTPUT: A barplot of the number of interactions TF-gene with each condifence

##UPDATE: 24/02/2023
     
##LOCATION EN GIT: https://github.com/PGC-CCG/supplementary-material/tree/master/golden-standard


library(dplyr)
df_NetWork = read.delim("../input/NetWorkTFGene.txt", 
                        skip=37, header = TRUE, sep = "\t", fill = TRUE)
View(df_NetWork)
#Filter and count the TF-gene interactions by confidence level
confidenceCountsNetwork<- df_NetWork %>%
  select(X7.confidenceLevel)%>%
  count(X7.confidenceLevel)
confidenceCountsNetwork<- confidenceCountsNetwork[order(confidenceCountsNetwork$n,
                                                        decreasing = TRUE), ]
confidenceCountsNetwork$color<-"grey" 
confidenceCountsNetwork$color[confidenceCountsNetwork$X7.confidenceLevel=="Confirmed"]<-"#af3508"
confidenceCountsNetwork$color[confidenceCountsNetwork$X7.confidenceLevel=="Strong"]<-"#57c101"
confidenceCountsNetwork$color[confidenceCountsNetwork$X7.confidenceLevel=="Weak"]<-"#0181c1"
#Plot the counts of TF-gene interactions by confidence level
par(mar=c(8,4,4,4))  
myBarplotconfidenceCountsNetwork<-barplot(height = confidenceCountsNetwork$n, 
names = confidenceCountsNetwork$X7.confidenceLevel,las=2, cex.main =.8, 
cex.names = .6, cex.axis = .6, cex.lab= .8, ylim=c(0,3200), 
ylab = "number of interactions", xlab = "Confidence level", 
col=confidenceCountsNetwork$color)
text(myBarplotconfidenceCountsNetwork, confidenceCountsNetwork$n +100, 
     paste(confidenceCountsNetwork$n) ,las=2, cex=.6)

