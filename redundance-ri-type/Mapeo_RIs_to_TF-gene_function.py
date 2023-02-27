'''
NAME
       Mapeo de RIs to TF-gene

VERSION
       0.1

AUTHOR
       Paloma Lara <palomalf86@gmail.com>

DESCRIPTION
       
CATEGORY
       mapping programs

USAGE
       program [OPTIONS]

ARGUMENTS

SOFTWARE REQUERIMENTS

INPUT
     El archivo descargable RISet.txt

OUTPUT
     Un archivo de mapeo indicando que RIs mapean
CREATION DATE
     30/01/23
     
LOCATION EN GIT https://github.com/larafp86/ pendiente
'''

import os
import pandas as pd

pd.set_option('display.max_columns',20)
pd.set_option('display.max_rows',50)

#dirs = os.listdir('../input/uniform_files')
df_all_tus = pd.DataFrame()
#Leer dataset de RIs y guardarlo en dataframe(A)
df_A= pd.read_csv("/Volumes/GoogleDrive/Shared drives/PGC-02.Proyectos_vigentes/Curacion/Analisis_HT_nuevo_conocimiento/3.Desarrollo/Golden_standard/Mapeo_TF-gene-to-RIs/input/RISet.txt", sep="\t", skiprows=54, header=0, encoding="utf-8")
print(df_A.shape)
df_A.head(n=5)
#Hacer una copia del dataframe de RIs(B)
df_B = df_A
print(df_B.shape)
#Genera el archivo de salida, abriendolo en modo de escritura
output_file = open("/Volumes/GoogleDrive/Shared drives/PGC-02.Proyectos_vigentes/Curacion/Analisis_HT_nuevo_conocimiento/3.Desarrollo/Golden_standard/Mapeo_TF-gene-to-RIs/output/TF_1gene_func_mapped_v1.txt","w")

#Escribe el encabezado
output_line = ( "tfName" + "\t" + "3)firt_gene" + "\t" + "riIds" + "\t"  + "riTypes"+  "\t" + \
              "tfrsLeft" + "\t" + "functions" + "\t"+  "confidenceLevels" + "\t"+  "matches" +"\n")
output_file.write(output_line)

#Recorrer dataframe A guardando en variables el TF y el firt gene (riId), guardar en el vector TF-firstgene, la información

#Proceso de mapeo
evaluated_TFgene = []
for index, row in df_A.iterrows():
    TF_A = row['4)tfName']
    firtgene_A = row['16)firstGene']
    rifunction_A=row["11)function"]
    pairTFgene=str(TF_A)+str(firtgene_A)+str(rifunction_A)
    tf_gene_match = 0
    if (pairTFgene not in evaluated_TFgene):
        evaluated_TFgene.append(pairTFgene)
        riids=[]
        ritypes=[]
        tfrslefts=[]
        functions=[]
        conflev=[]
        #Recorrer el dataframe B guardando en variables el TF, el first, gene el riId, riType, Tfrs left, function
        for index2, row in df_B.iterrows():
            TF_B = row['4)tfName']
            firtgene_B = row['16)firstGene']
            riID_B = row['1)riId']
            riType_B = row['2)riType']
            tfrsLeft_B = row['7)tfrsLeft']
            functionB = row['11)function']
            confidence_level = row['19)confidenceLevel'] 
            if (TF_A == TF_B) & (firtgene_A==firtgene_B)& (rifunction_A==functionB):
                tf_gene_match+=1
                riids.append(riID_B)
                ritypes.append(riType_B)
                tfrslefts.append(tfrsLeft_B)
                functions.append(functionB)
                conflev.append(confidence_level)
            else: 
                continue

        output_line1 = ( str(TF_A) + "\t" + str(firtgene_A)  + "\t" + str(riids) + "\t"  + str(ritypes) +  "\t" + \
              str(tfrslefts)  + "\t" + str(functions)  + "\t"+  str(conflev)  + "\t"+  str(tf_gene_match)  +"\n")
        outputline2= output_line1.replace("[", "")
        output_line3= outputline2.replace("]", "")
        print(output_line3)
        output_file.write(output_line3)
        
    else: 
                    continue
        
output_file.close()
print("Terminado")
