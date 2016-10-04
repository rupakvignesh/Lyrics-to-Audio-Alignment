# Wrapper script for forced alignment

#Create directories
sh scripts/clean_dir.sh
sh scripts/create_directories.sh

#Copy wav and extract features
sh scripts/extract_features.sh

#Convert labels
python scripts/timit_alignments_to_htk.py

#Create MLFs
python scripts/create_transcription.py

#Prepare phonelist, dict
cat mfc_train/*.lab | cut -d " " -f3 | sort | uniq > lists/phonelist
paste lists/phonelist lists/phonelist > lists/dict
cd mfc_train; ls *.lab > ../lists/lablist.train; cd ../
cd mfc_test; ls *.lab > ../lists/lablist.test; cd ../


#TRAINIG
tcsh scripts/model_gen.sh lists/phonelist proto_6s_4m		#Arg1=phonelist Arg2=proto

#Embedded reestimation
iter=10
tcsh scripts/embedded_reestimation.sh $iter


#TESTING
echo "Sentence Lvl Alignment"
HVite -T 1 -l output_lab_train/ -C Configs/config-hvite -a -H hmm_with_er/hmm$iter/hmmdefs -y lab -o MN -I words.mlf -S lists/mfclist_formatted.train lists/dict lists/phonelist
HVite -T 1 -l output_lab_test/ -C Configs/config-hvite -a -H hmm_with_er/hmm$iter/hmmdefs -y lab -o MN -I test.mlf -S lists/mfclist_formatted.test lists/dict lists/phonelist


