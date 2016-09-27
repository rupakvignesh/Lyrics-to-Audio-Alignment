#Wrapper script for forced alignment

#create directories
sh scripts/clean_dir.sh
sh scripts/create_directories.sh

#copy wav and extract features
sh scripts/extract_features.sh

#convert labels
python scripts/timit_alignments_to_htk.py


#prepare phonelist, dict
cat mfc_train/*.lab | cut -d " " -f3 | sort | uniq > lists/phonelist
paste lists/phonelist lists/phonelist > lists/dict


#TRAINIG
tcsh scripts/model_gen.sh lists/phonelist proto_5s_2m		#Arg1=phonelist Arg2=proto

#TESTING
echo "Sentence Lvl Alignment"
HVite -l output_lab/ -C Configs/config-hvite -a -H hmm/hmmdefs -y lab -o MN -I words.mlf -S lists/mfclist_formatted.train lists/dict lists/phonelist
