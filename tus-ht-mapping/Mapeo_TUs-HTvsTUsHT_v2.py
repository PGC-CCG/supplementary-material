'''
NAME
       Mapeo de TUs-HT vs TUs-HT

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

IMPUT
     Un directorio con datasets de TUs-HT uniformizados(RegulonDB11.0), deben tener las mismas columnas 
     y estas deben llamarse como se indica en el script
     

OUTPUT
     Un archivo de mapeo de TUs
CREATION DATE
     17/11/2022
     
LOCATION EN GIT https://github.com/larafp86/
'''

import os
import pandas as pd

pd.set_option('display.max_columns',20)
pd.set_option('display.max_rows',50)
directory_path= '../input/uniform_files/'
dirs = os.listdir('../input/uniform_files')
df_all_tus = pd.DataFrame()

#Lee todos los datasets de TUs y los concatena en un solo dataframe
for d in dirs:
    file= directory_path + str(d)
    df_new= pd.read_csv(file, sep="\t", header=0, encoding="utf-8")
    print(df_new.shape)
    df_all_tus = pd.concat([df_all_tus, df_new])
#Genera una copia del dataframe con los datasets concatenados
df_all_tus2 = df_all_tus
print(df_all_tus2.shape)
#Genera el archivo de salida, abriendolo en modo de escritura
output_file = open("../output/TUsHT-TUsHT_map_genes_v0.1.txt","w")

#Escribe el encabezado
output_line = ("TU_ID" + "\t" + "TU_posleft" + "\t" + "TU_posright" + "\t" + \
              "TU_strand" + "\t" + "TU_Numb_genes" + "\t"+ "TU_genes"+ "\t" + \
                "TU_ID_match" + "\t" + "TU_posleft_match" + "\t" + "TU_posright_match" + "\t" + \
              "TU_strand_match" + "\t"+ "TU_n_g_match" + "\t"+ "TU_genes_match"+ "\n")
output_file.write(output_line)

#Estos son los parametros de mapeo
start_maximum_distance = 5
stop_maximum_distance = 300

#Proceso de mapeo
evaluated_tus_parir = []
for index, row in df_all_tus.iterrows():
    tu_id = row['id']
    tu_start = row['start']
    tu_stop = row['stop']
    tu_strand = row['strand']
    tu_number_genes= row['gene_number']
    tu_genes=row['genes']
    tu_match = 0
    for index2, row in df_all_tus2.iterrows():
        tu_id2 = row['id']
        tu_start2 = row['start']
        tu_stop2 = row['stop']
        tu_strand2 = row['strand']
        tu_number_genes2= row['gene_number']
        tu_genes2=row['genes']
        start_distance=abs((tu_start)-(tu_start2))
        stop_distance=abs((tu_stop)-(tu_stop2))
        pair1=str(tu_id)+str(tu_id2)
        pair2=str(tu_id2)+str(tu_id)
        if tu_id!=tu_id2:
            if (start_distance <= start_maximum_distance) & (stop_distance <= stop_maximum_distance) & (tu_strand == tu_strand2):
                tu_match+=1
                #Escribe en el archivo de salida los pares de TUs que mapean
                output_line = (tu_id + "\t" + str(tu_start) + "\t" + str(tu_stop) + "\t" + tu_strand + "\t" + str(tu_number_genes) + \
                    "\t" + str(tu_genes) + "\t" + tu_id2 + "\t" + str(tu_start2) + "\t" + str(tu_stop2) + "\t" + tu_strand2 + "\t" + \
                        str(tu_number_genes2) + "\t" + str(tu_genes2) + "\n")
                if (pair1 not in evaluated_tus_parir) & (pair2 not in evaluated_tus_parir):
                    output_file.write(output_line)
                    evaluated_tus_parir.append(pair1)
                    evaluated_tus_parir.append(pair2)
                    print(output_line)
                else: 
                    continue
            else:
                continue
        else:
            continue
    if tu_match == 0:
        #Escribe en el archivo de salida las TUs que no mapean con ninguna otra indicando null en las columnas de match
        output_line2 = (tu_id + "\t" + str(tu_start) + "\t" + str(tu_stop) + "\t" + tu_strand + "\t" + str(tu_number_genes) + "\t" + \
             str(tu_genes) + "\t" + "null" + "\t" + "null" + "\t" + "null" + "\t" + "null" + "\t" + "null" + "\t" + "null" + "\n")
        output_file.write(output_line2)
    else:
        continue
#Fin, se cierra el archivo de salida
output_file.close()
print("Terminado")
