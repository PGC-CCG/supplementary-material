import pandas as pd
import shutil, os
import time
import datetime
import re
import UpdateCoordinates
import traceback

#print (os.getcwd())

#Base path for scripts
scripts_base_path="C:/Users/cbona/OneDrive/Documentos/GitHub/regulondb-data-pipelines/TU-match-maker/Cesar-Tests/Format-AuthorFiles_from_Metadata_and_CoordinatesUpdate-MOD202307"

#Change directory to Scripts Directory
os.chdir(scripts_base_path)


#Base path for Input Files
input_files_base_path="G:/Shared drives/PGC-02.Proyectos_vigentes/Curacion/Curación_HT_pl/curation_datasets-HT/3.Desarrollo/DatasetsTFBSRegulonDB11.1"
print("\nInput Directory: \n" + input_files_base_path)

#Base path for Output Files
output_files_base_path="G:/Shared drives/PGC-02.Proyectos_vigentes/Curacion/Curación_HT_pl/curation_datasets-HT/3.Desarrollo/DatasetsTFBSRegulonDB11.1"
print("\nOutput Directory: \n" + output_files_base_path + "\n")

U000962_to_U000963_file = input_files_base_path + "/coordinate_updates" + "/U00096.2_to_U00096.3.tsv"
NC_0077791_to_U000963_file = input_files_base_path + "/coordinate_updates" + "/NC_007779.1_to_U00096.3.tsv"

U000962_to_U000963_info = "|U00096.2|U00096.3|"+U000962_to_U000963_file
NC_0077791_to_U000963_info ="|NC_007779.1|U00096.3|"+NC_0077791_to_U000963_file

# Used during develpment to limit the number of files to be processed. (Leave -1 to process all files)
max_files = -1

# Used during develpment to skip certain number of rows from the metadata. (Leave -1 to process all files)
skip_to_metadata_row = -1

# This variable is used during development to limit the number of rows to be processed in each file.
# Leave -1 to process all rows in the files.
max_rows = -1

# This variable is used during development to limit the number of last rows to be processed in each file.
# Leave -1 to process all rows in the files.
last_rows = -1

# This variable is used to run the scripts against a specific set of data instead of the full
# array of records included in the Metadata.
# If this is a TEST execution, then we need to use the metadata containing TEST cases.
test_run = "no"

input_version="_v3.0"
output_version="_v4.0"

mapping_log_file_txt = output_files_base_path + "/Validate-Coordinate-Updates_LOG.txt"

txt_log_file_handler = open(mapping_log_file_txt, "w")
txt_log_file_handler.write("Validate-Coordinate-Updates Log\n")
txt_log_file_handler.write("Start time: " + str(datetime.datetime.now()) + "\n")



def main():
  try:

    test_coordinates = [
        "257905"+U000962_to_U000963_info, ##Resultado Esperado: 257905
        "257906"+U000962_to_U000963_info, ##Resultado Esperado: 257906
        "257907"+U000962_to_U000963_info, ##Resultado Esperado: 257907
        "257908"+U000962_to_U000963_info, ##Resultado Esperado: 258684
        "257909"+U000962_to_U000963_info, ##Resultado Esperado: 258685
        "257910"+U000962_to_U000963_info, ##Resultado Esperado: 258686
        "275911"+U000962_to_U000963_info, ##Resultado Esperado: 258687
        "275912"+U000962_to_U000963_info, ##Resultado Esperado: 258688
        "275913"+U000962_to_U000963_info, ##Resultado Esperado: 258689
        "275914"+U000962_to_U000963_info, ##Resultado Esperado: 258690
        "275915"+U000962_to_U000963_info, ##Resultado Esperado: 258691
        "257905"+NC_0077791_to_U000963_info, ##Resultado Esperado: 257905
        "257906"+NC_0077791_to_U000963_info, ##Resultado Esperado: 257906
        "257907"+NC_0077791_to_U000963_info, ##Resultado Esperado: 257907
        "257908"+NC_0077791_to_U000963_info, ##Resultado Esperado: 258684
        "257909"+NC_0077791_to_U000963_info, ##Resultado Esperado: 258685
        "257910"+NC_0077791_to_U000963_info, ##Resultado Esperado: 258686
        "275911"+NC_0077791_to_U000963_info, ##Resultado Esperado: 258687
        "275912"+NC_0077791_to_U000963_info, ##Resultado Esperado: 258688
        "275913"+NC_0077791_to_U000963_info, ##Resultado Esperado: 258689
        "275914"+NC_0077791_to_U000963_info, ##Resultado Esperado: 258690
        "275915"+NC_0077791_to_U000963_info, ##Resultado Esperado: 258691
        "547692"+NC_0077791_to_U000963_info,  ##Resultado Esperado: 548468
        "547693"+NC_0077791_to_U000963_info,  ##Resultado Esperado: 548469
        "547694"+NC_0077791_to_U000963_info,  ##Resultado Esperado: >>>>>>>NOT FOUND
        "547695"+NC_0077791_to_U000963_info,  ##Resultado Esperado: 548471
        "547696"+NC_0077791_to_U000963_info,  ##Resultado Esperado: 548472
        "1093684" + NC_0077791_to_U000963_info,  ##Resultado Esperado: 1093262
        "1093685" + NC_0077791_to_U000963_info,  ##Resultado Esperado: 1093263
        "1093686" + NC_0077791_to_U000963_info,  ##Resultado Esperado: >>>>>>>NOT FOUND
        "1093687" + NC_0077791_to_U000963_info,  ##Resultado Esperado: 1093265
        "1093688" + NC_0077791_to_U000963_info,  ##Resultado Esperado: 1093266
        "1105620" + NC_0077791_to_U000963_info,  ##Resultado Esperado: 1105379
        "1105621" + NC_0077791_to_U000963_info,  ##Resultado Esperado: 1105380
        "1105622" + NC_0077791_to_U000963_info,  ##Resultado Esperado: >>>>>>>NOT FOUND
        "1105623" + NC_0077791_to_U000963_info,  ##Resultado Esperado: >>>>>>>NOT FOUND
        "1105624" + NC_0077791_to_U000963_info,  ##Resultado Esperado: >>>>>>>NOT FOUND
        "1105625" + NC_0077791_to_U000963_info,  ##Resultado Esperado: >>>>>>>NOT FOUND
        "1105700" + NC_0077791_to_U000963_info,  ##Resultado Esperado: >>>>>>>NOT FOUND
        "1105800" + NC_0077791_to_U000963_info,  ##Resultado Esperado: >>>>>>>NOT FOUND
        "1105900" + NC_0077791_to_U000963_info,  ##Resultado Esperado: >>>>>>>NOT FOUND
        "1106000" + NC_0077791_to_U000963_info,  ##Resultado Esperado: >>>>>>>NOT FOUND
        "1106500" + NC_0077791_to_U000963_info,  ##Resultado Esperado: >>>>>>>NOT FOUND
        "1106900" + NC_0077791_to_U000963_info,  ##Resultado Esperado: >>>>>>>NOT FOUND
        "1106940" + NC_0077791_to_U000963_info,  ##Resultado Esperado: >>>>>>>NOT FOUND
        "1106950" + NC_0077791_to_U000963_info,  ##Resultado Esperado: >>>>>>>NOT FOUND
        "1106951" + NC_0077791_to_U000963_info,  ##Resultado Esperado: >>>>>>>NOT FOUND
        "1106957" + NC_0077791_to_U000963_info,  ##Resultado Esperado: >>>>>>>NOT FOUND
        "1106958" + NC_0077791_to_U000963_info,  ##Resultado Esperado: 1105381
        "1106959" + NC_0077791_to_U000963_info,  ##Resultado Esperado: 1105382
        "1106960" + NC_0077791_to_U000963_info  ##Resultado Esperado: 1105383
    ]

#    for current_coordinate in test_coordinates:
#        (coordinate_to_update, reference_genome_to_update, updated_reference_genome,reference_genome_to_update_file) = current_coordinate.split("|")
#        Test_UpdateCoordinates(coordinate_to_update, reference_genome_to_update, updated_reference_genome,reference_genome_to_update_file)


    collections = [
        "Test-seq" + NC_0077791_to_U000963_info
#        ,
#        "gSELEX"+NC_0077791_to_U000963_info
#        ,
#        "ChIP-exo"+U000962_to_U000963_info
#        ,
#        "ChIP-seq"+U000962_to_U000963_info
#        ,
#        "DAP-seq"+U000962_to_U000963_info
    ]

    for current_collection in collections:
        (current_author_data, reference_genome_to_update, updated_reference_genome,reference_genome_to_update_file) = current_collection.split("|")
        process_author_data(current_author_data, reference_genome_to_update, updated_reference_genome,reference_genome_to_update_file)

    txt_log_file_handler.write("==============\n============\nRun-Coordinate-Updates Log\n")
    txt_log_file_handler.write("END TIME: " + str(datetime.datetime.now()) + "\n")
    txt_log_file_handler.close()


  except (Exception) as e:
     print(e)
     print(traceback.format_exc())

def process_author_data (current_author_data, reference_genome_to_update, updated_reference_genome,reference_genome_to_update_file):
  try:
    #DP
    print ("current_author_data: ",current_author_data)

    #DP
    print ("reference_genome_to_update: ", reference_genome_to_update)

    #DP
    print ("updated_reference_genome: ", updated_reference_genome)

    #DP
    print ("reference_genome_to_update_file: ", reference_genome_to_update_file)

    input_files_dir =  input_files_base_path +"/" + current_author_data+"/Dataset_author_files/"+current_author_data + input_version

    #Debugging Purposes (DP)
    #print("\n"+author_files_directory+"\n")

    #####
    updated_coordinates_directory =  output_files_base_path +"/" + current_author_data+"/Dataset_author_files/"+current_author_data + output_version


    #SET Metadata Path.
    # If this is a TEST execution, then we need to use the metadata containing TEST cases.
    if (test_run == "yes"):
        # If this is a TEST execution, use metadata containing TEST cases
        metadata_path = input_files_base_path + "/" + current_author_data + "/Metadata/Test"
        print("metadata_path: " + metadata_path)
    else :
        metadata_path = input_files_base_path + "/" + current_author_data + "/Metadata"

    #Get metadata contents
    (df_metadata, metadata_file_name) = get_metadata(metadata_path)

    #Debugging Purposes (DP)
    ###print (df_metadata)

    #Directory and report file to store the coordinates updating process log.
    log_dir = output_files_base_path + "/" + current_author_data + "/Analysis"

    #Archivo de reporte temporal únicamente para reportar posibles errores durante la ejecución de la conversión de coordenadas.
    coordinates_update_log_file = log_dir + "/" + current_author_data+ "_CoordinatesUpdate_LOG.txt"

    txt_log_file_handler = open(coordinates_update_log_file, "w")
    txt_log_file_handler.write("Coordinates Update Log\n")
    txt_log_file_handler.write("Start time: "+ str(datetime.datetime.now()) +"\n")

    print("\n==============\nCoordinates_Update_log_file: ", coordinates_update_log_file+"\n==============\n")


    count_metadata_rows=0

    #For each row contained in the list of TFs and Files (Metadata) to evaluate for the current author data:
    for index, row in df_metadata.iterrows():

        count_metadata_rows=count_metadata_rows+1

        # Sólo durante desarrollo
        # LIMITA el procesamiento a únicamente "max_files" archivos de entrada
        # Para procesar todos los archivos, max_files debe tener un valor de -1
        if index==max_files:
            break

        # Used during develpment to skip certain number of rows from the metadata. (Leave -1 to process all files)
        if index<=skip_to_metadata_row :
            continue

        print("===========================\n")

        # Get the content of column "RegulonDB_TF_MainName" which in this case is
        # the Main Name of the TF in RegulonDB.
        metadata_tf_main_name = str(df_metadata.loc[index, 'RegulonDB TF Name']).strip()
        #DP
        print("metadata_tf_main_name: ",metadata_tf_main_name)

        # Get the content of column "Reference genome" which is used to determine whether the file contains
        # coordinates to convert or not.
        metadata_reference_genome = str(df_metadata.loc[index, 'Source reference genome']).strip()
        #DP
        #print("metadata_reference_genome: ",metadata_reference_genome)

        #Get the contents of column "Dataset File Name" which contains the name of the file to process.
        current_authors_data_file = str(df_metadata.loc[index, 'Dataset File Name']).strip()
        #DP
        #print("current_authors_data_file: ",current_authors_data_file)

        #If there is NO filename in the Metadata for a particular TF, then this should be reported and continue with the next metadata row.
        if str(current_authors_data_file)=="nan":
            error_log="ERROR. There is no file name for TF: "+metadata_tf_main_name+" in "+ current_author_data + " --- Metadata file: "+ metadata_file_name + "\n\n"
            print (error_log)
            txt_log_file_handler.write(error_log)
            continue

        # Remove the file name extension, so we can use the corresponding extension
        current_authors_data_file_wo_extension = os.path.splitext(current_authors_data_file)[0]
        #DP
        print("current_authors_data_file_wo_extension: ",current_authors_data_file_wo_extension)

        #Build the complete path to the file to be processed.
        author_file_name_for_coordinates_update = input_files_dir+"/" + current_authors_data_file_wo_extension + ".xlsx"

        print("\nWorking on author_file_name_for_coordinates_update: ", author_file_name_for_coordinates_update)

        output_updated_authorFile_xlsx = updated_coordinates_directory + "/" + current_authors_data_file_wo_extension +".xlsx"

        print("\nOutput File: ",output_updated_authorFile_xlsx)

        #Verifying if the Reference Genome for the current metadata record is going to be updated:
        if metadata_reference_genome != reference_genome_to_update:
            # If the reference genome of the author file is other than the one to process then:
            # 1) Report it on the Log File;
            # 2) Copy the unprocessed file to the destination directory.
            # 3) continue with the next record.
            # Report finding multiple TFs for current TF.
            log_text = "\nWARNING. " + current_author_data + " file's Reference Genome for TF: " + metadata_tf_main_name + \
                       " WAS NOT UPDATED. The file will be copied to the destination folder. " + \
                       " Current file's reference genome is: " + metadata_reference_genome + \
                       " --- Data File: " + current_authors_data_file_wo_extension + ".xlsx" + "\n\n"
            # 1) Report it on the Log File;
            print(log_text)
            txt_log_file_handler.write(log_text)
            # 2) Copy the unprocessed file to the destination directory.
            #First verify that the file to be copied exists on the origin.
            if os.path.isfile(author_file_name_for_coordinates_update):
                #File exists on the origin, so will be copied to the destination directory.
                shutil.copyfile(author_file_name_for_coordinates_update,output_updated_authorFile_xlsx)
            else :
                #File does not exist on the origin. Report it to the LOG FILE.
                error_log = "ERROR. Could NOT FIND " + current_author_data + " file: " + author_file_name_for_coordinates_update + " -- TF: " + metadata_tf_main_name + " --- Metadata file: " + metadata_file_name + "\n\n"
                print(error_log)
                txt_log_file_handler.write(error_log)

            # 3) continue with the next record.
            continue


        if os.path.isfile(author_file_name_for_coordinates_update):
            df_input_file_for_coord_updt = pd.read_excel(author_file_name_for_coordinates_update, sheet_name=0, header=0)

            #DP
            print("\n\nDATA FRAME del archivo a convertir: df_input_file_for_coord_updt:\n\n" , df_input_file_for_coord_updt)

            #####If this is a Test-seq file then keep selected colums as "Original columns"
            # In the current Test case we will keep Peak_start and Peak_end
            if current_author_data == "Test-seq":
                # Duplicate column 'Peak center' as 'Peak center' in TEC datababase' to keep the original values.
                df_input_file_for_coord_updt['Original Peak start'] = df_input_file_for_coord_updt.loc[:,'Peak_start']
                df_input_file_for_coord_updt['Original Peak end'] = df_input_file_for_coord_updt.loc[:,'Peak_end']

                # DP
                print("df_input_file_for_coord_updt COLUMNS:", df_input_file_for_coord_updt)

            #####If this is a gSELEX file then DO NOT UPDATE THE Peak center value but
            # copy "peak center" value into "Peak center in TEC datababase"
            # and then update "Peak center" column with updated value (same as with other author data files)
            if current_author_data=="gSELEX":
                #Duplicate column 'Peak center' as 'Peak center' in TEC datababase' to keep the original values.
                df_input_file_for_coord_updt['Peak center in TEC datababase']=df_input_file_for_coord_updt.loc[:,'Peak center']

                #DP
                #print("df_input_file_for_coord_updt: BEFORE REORDERING COLUMNS",df_input_file_for_coord_updt)

                reorder_columns=["TF_name*","Peak_start", "Peak_end","Co-ordinates",
                    "Peak center in TEC datababase", "Peak center", "Peak Maximum Coverage Position", "Peak length",
                    "Peak number", "Peak-Shape score", "Peak Coverage", "Peak Intensity Fold Change/Binding intensity (%)", "S/N ratio (Enrichment)",
                    "p-value", "Target gene*", "GCs (Control)*", "GCs (Experimental)*", "Evidence for binding* (Method)",
                    "Sequence", "Score", "TFBS_position (Motif center locus)", "Motif start distance", "Evidence for binding site",
                    "site start", "site end", "Function", "Evidence for function",
                    "No. Fragments cloned from gSELEX", "peak strand", "Motif strand", "Peak Location Relative to Gene",
                    "FC", "Log2 FC", "Operon", "TF Main Name",
                    "RI EVIDENCE TYPE IN REGULONDB", "RI EFFECT IN REGULONDB"]
                df_input_file_for_coord_updt=df_input_file_for_coord_updt[reorder_columns]

                #DP
                #print("df_input_file_for_coord_updt: AFTER REORDERING COLUMNS",df_input_file_for_coord_updt)


            #Copy the columns of the file to convert.
            df_input_file_WITH_updt_coord = pd.DataFrame(data=None, columns=df_input_file_for_coord_updt.columns)

            #DP
            #print("\n\nDATA FRAME del archivo de salida: df_input_file_WITH_updt_coord:\n\n" , df_input_file_WITH_updt_coord)

        else :
            error_log="ERROR. Could NOT FIND "+ current_author_data + " file: "+author_file_name_for_coordinates_update + " -- TF: "+metadata_tf_main_name + " --- Metadata file: "+ metadata_file_name + "\n\n"
            print (error_log)
            txt_log_file_handler.write(error_log)
            continue

        #DP -- Number of TF / Filename Pair:
        print("\n---------Processing "+current_author_data+" collection. Record No= " + str(index) + \
              " (#of row in Excel File = "+str(index+2)+") -- "+ \
              "TF in RegulonDB: "+metadata_tf_main_name+"; File: "+current_authors_data_file+"; Metadata: "+metadata_file_name+"\n")



        # For each row in the file to be updated, we need to:
        # 1. Keep all columns values, except those that contain any kind of coordinate:
        # Peak_start
        # Peak_end
        # Coordinates
        # Peak center
        # Peak Maximum Coverage Position
        # TFBS_position(Motif center locus)
        # site start
        # site end

        columns = [
          "Peak_start",
          "Peak_end",
          "Co-ordinates",
          "Peak center",
          "Peak Maximum Coverage Position",
          "TFBS_position (Motif center locus)",
          "site start",
          "site end"
        ]

        #####If this is a Test-seq file then RE-DEFINE the columns to test
        if current_author_data == "Test-seq":
            columns = [
                "Peak_start",
                "Peak_end"
            ]

        #Initialize variable to count the number of rows that have been processed in the current file.
        processed_rows=-1

        #This part is used to skip as many rows to get to the given number of "last_rows" to be processed in a file.
        #This is just used during development to reduce the execution time.
        if last_rows > 0:
            #DP to test the use of LEN to count the number of records in a Data Frame
            # print("Total Rows (len): " + str(len(df_input_file_for_coord_updt.index)))

            #DP to test the use of SHAPE attribute to count the number of records in a Data Frame
            print("Total Rows (shape): " + str(df_input_file_for_coord_updt.shape[0]))

            #Set the number of rows to which the process should skip during development (last_rows>0).
            #This is just used for developing purposes (to test run without processing all records)
            processed_rows = df_input_file_for_coord_updt.shape[0] - last_rows -1
            print("Skip to row: "+str(processed_rows))

        finished_with_errors = 0
        for index2, row2 in df_input_file_for_coord_updt.iterrows():

            #If not yet in the configured last_rows value then skip record.
            #This is just used for developing purposes (to test run without processing all records)
            if last_rows>0 and index2<=processed_rows :
                #DP
                # print("index2 (SKIPED): "+str(index2))
                continue

            processed_rows=processed_rows+1
            #DP
            # print("Processing Row (index2): "+str(index2))
            print("Processing Row (processed_rows): "+str(processed_rows))


            #Get the complete record for the current  formatted author file.
            df_current_record = df_input_file_for_coord_updt.loc[index2]

            #DP
            #print ("\n\ndf_current_record ANTES DE CONVERTIR COORDENADAS: \n\
            for current_column in columns:
                if str(df_current_record[current_column])!="nan" :

                    updated_coordinate = UpdateCoordinates.Update_Coordinate(reference_genome_to_update_file,df_current_record[current_column])
                    if str(updated_coordinate)=="Not found":
                        error_log = "\nERROR. Coordinate WAS NOT FOUND. (" + current_author_data + ") file: " + \
                                    author_file_name_for_coordinates_update + " -- TF: " + metadata_tf_main_name + \
                                    " --- Metadata file: " + metadata_file_name + \
                                    "\n************df_current_record["+current_column+"]: " + str(df_current_record[current_column]) + \
                                    " --->>> "+ str(updated_coordinate) + "\n\n"
                        print(error_log)
                        txt_log_file_handler.write(error_log)
                        df_current_record[current_column] = "NOT FOUND"
                        finished_with_errors=finished_with_errors+1
                        continue

                    # DP
                    print ("\n************df_current_record["+current_column+"]: " + str(df_current_record[current_column]) + \
                            " --->>> "+ str(updated_coordinate))

                    df_current_record[current_column] = updated_coordinate

            #DP
            #print ("\ndf_current_record DESPUES DE CONVERTIR COORDENADAS: \n\n", df_current_record)

            df_input_file_WITH_updt_coord = df_input_file_WITH_updt_coord.append(df_current_record, ignore_index=True)

            # Sólo durante desarrollo
            # LIMITA el procesamiento a únicamente "max_rows" registros del archivo de entrada
            # Para procesar todos los registros, max_rows debe tener un valor de -1
            if index2==max_rows:
                break

        # #Store the new updated datafile
        df_input_file_WITH_updt_coord.to_excel(output_updated_authorFile_xlsx, index=False)

        if finished_with_errors==0 :
            log_text = "\nUPDATE REPORT. " + current_author_data + " file's Reference Genome for TF: " + metadata_tf_main_name + \
               " WAS CORRECTLY UPDATED from: " + metadata_reference_genome + " to: " + updated_reference_genome + "\n" + \
               " --- Data File: " + current_authors_data_file + "\n"
        else :
            log_text = "\nUPDATE REPORT WITH ERRORS. " + current_author_data + " file's Reference Genome for TF: " + metadata_tf_main_name + \
                       " WAS UPDATED WITH " + str(finished_with_errors) + " Coordinates NOT FOUND. from: " + metadata_reference_genome + \
                       " to: " + updated_reference_genome + "\n" + \
                       " --- Data File: " + current_authors_data_file + "\n"

        print(log_text)
        txt_log_file_handler.write(log_text)


    log_text="\n=======\nMetadata rows: "+str(count_metadata_rows) +\
             "\nmaxfiles: "+str(max_files)+"\nskip_to_metadata_row: "+str(skip_to_metadata_row) +\
             "\nmax_rows: "+str(max_rows)+ \
             "\nlast_rows: " + str(last_rows) + "\n"

    print(log_text)
    txt_log_file_handler.write(log_text)

    log_text="End time: "+ str(datetime.datetime.now()) +"\n"
    print(log_text)
    txt_log_file_handler.write(log_text)
    #Close the log file
    txt_log_file_handler.close()


  except (Exception) as e:
     print(e)
     print(traceback.format_exc())


def get_metadata(metadata_path):
    metadata_file_name = ""
    for current_file_in_metadata_path in os.listdir(metadata_path):
        if current_file_in_metadata_path.endswith(".xlsx"):
          if current_file_in_metadata_path.startswith("~$"):
            continue
          else :
            print("Using the next METADATA FILE in: ", current_file_in_metadata_path)
#            df_metadata=pd.read_excel(metadata_path+"/"+current_file_in_metadata_path, sheet_name="DATASET", skiprows=3, header=0)
            df_metadata=pd.read_excel(metadata_path+"/"+current_file_in_metadata_path, sheet_name="DATASET", comment='#', header=0)
            metadata_file_name = current_file_in_metadata_path
#DP
#            print(df_metadata)
            break


    return df_metadata, metadata_file_name


def Test_UpdateCoordinates(coordinate_to_update, reference_genome_to_update, updated_reference_genome,reference_genome_to_update_file) :
  try:

    updated_coordinate=UpdateCoordinates.Update_Coordinate(reference_genome_to_update_file,int(coordinate_to_update))

    #DP
    print("Received coordinate ("+reference_genome_to_update+"): " + str(coordinate_to_update) + \
          "; Updated Coordinate ("+updated_reference_genome+"): " + str(updated_coordinate) + \
          "; Used file: " + reference_genome_to_update_file)
    return updated_coordinate

  except (Exception) as e:
     print(e)
     print(traceback.format_exc())
     txt_log_file_handler.write(e)
     txt_log_file_handler.write(traceback.format_exc())


if __name__ == "__main__":
    main()
