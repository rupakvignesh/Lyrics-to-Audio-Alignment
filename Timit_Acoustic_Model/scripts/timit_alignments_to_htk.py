# Converts the alignment file in timit (.phn)
# to htk format (.lab).
# Timit alignments: [start_sample_ind end_sample_ind phone_label]
# HTK format: [start_time(100ns) end_time(100ns) phone_label] 
# Replaces h# with sil
# Author: Rupak Vignesh

import os

#Source directory
Timit_dir = "/Users/RupakVignesh/Documents/TIMIT" 

#Destination directory
HMM_dir = "/Users/RupakVignesh/Desktop/7100/Lyrics-to-Audio-Alignment/Timit_Acoustic_Model"

#Global variables
sampling_rate = 16000 					#Sampling rate of the wav files in Hertz


def convert_labels(database):
    db_dir = os.path.join(Timit_dir,database)		        #database = "train" or test" 
    phn_list = []						#Get list of *.phn file along with their location
    for dr_dir in os.listdir(db_dir):
        dr_path = os.path.join(db_dir,dr_dir)		        #appends dir name to the path
        if os.path.isdir(dr_path):                              #Check if a file is directory
            for spkr_dir in os.listdir(dr_path):
                spkr_path = os.path.join(dr_path,spkr_dir)
                if os.path.isdir(spkr_path):
                    for file in os.listdir(spkr_path):
                        if file.endswith(".phn"):
                            file_path = os.path.join(spkr_path,file)
                            phn_list.extend([file_path])	# file(and location) is appended to the phn_list
    
    for i in range(len(phn_list)):
        with open(phn_list[i],'r') as PHN_FILE:
            phn_content = PHN_FILE.readlines()
            phn_content_parsed = []
            for j in range(len(phn_content)): 
                phn_content_parsed.extend([str.split(phn_content[j])])
            lab_name_temp = str.split(phn_list[i],'/')       	#splits the path on the delimiter '/'
            lab_name = lab_name_temp[-1][:-3]+'lab'    		#renames the .phn to .lab
            dr_spkr_id = '_'.join(lab_name_temp[-3:-1])         #Joins dialect and spkr ids
            op_file_name = dr_spkr_id + '_' + lab_name
            lab_file = open(HMM_dir+'/mfc_'+database+'/'+op_file_name,'a')
            for j in range(len(phn_content_parsed)):
                start_time = (float(phn_content_parsed[j][0])/sampling_rate)*pow(10,7)        # sample index to 100 nano seconds
                end_time = (float(phn_content_parsed[j][1])/sampling_rate)*pow(10,7)
                phn_label = phn_content_parsed[j][2]      
                #print start_time, end_time, phn_content_parsed[j][2]                         # phn_content_parsed[i][3] = phone label
                if(phn_label=="h#"):
                    lab_file.write(str(start_time) + " " + str(end_time) + " sil\n")
                else:
                    lab_file.write(str(start_time) + " " + str(end_time) + " " + phn_label + "\n")
            lab_file.close()

convert_labels("train")
#convert_labels("test")


