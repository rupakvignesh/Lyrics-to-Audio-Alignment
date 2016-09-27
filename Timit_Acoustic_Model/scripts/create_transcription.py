# Creates Master label file (MLF)
# MLF - sequence of phone labels of all
# lab files.
#
# Author: Rupak Vignesh

import os

#label file directory
hmm_dir = '/Users/RupakVignesh/Desktop/7100/Lyrics-to-Audio-Alignment/Timit_Acoustic_Model'
lab_dir = os.path.join(hmm_dir,'mfc_train/')


with open(hmm_dir+'/words.mlf','a') as mlf_file:
    mlf_file.write("#!MLF!#\n")						#MLF header

    for file in os.listdir(lab_dir):
        if(file.endswith('.lab')):
            print file
            lab_path = os.path.join(lab_dir,file)
            with open(lab_path,'r') as lab_file:
                lab_content = lab_file.readlines()
            lab_content_parsed = []
            mlf_file.write('"*/' + file +'"\n')				#File location
            for i in range(len(lab_content)): 				#File contents (labels)
                lab_content_parsed.extend([str.split(lab_content[i])])
                mlf_file.write(lab_content_parsed[i][2]+'\n')		#lab_content_parsed[i][2] = phone label
            mlf_file.write(".\n")

    mlf_file.close()
 
