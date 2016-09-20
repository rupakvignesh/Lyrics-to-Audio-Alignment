#!/bin/sh

# Converts sph to riff format using sph2pipe
# Extracts mfcc using HCopy
# Author: Rupak Vignesh

#Input paths
TIMIT_DIR=/Users/RupakVignesh/Documents/TIMIT
SPH_DIR=/Users/RupakVignesh/Documents/sph2pipe_v2.5

TRAIN_DIR=$TIMIT_DIR/train
TEST_DIR=$TIMIT_DIR/test
HMM=/Users/RupakVignesh/Desktop/7100/LyricAlignment/code/Timit_Acoustic_Model

echo "Copying wav and extracting features"


find $TRAIN_DIR -type f -name '*.wav' > $HMM/lists/wavlist_timit.train
#find $TEST_DIR -type f -name '*.wav' > $HMM/lists/wavlist_timit.test

#Copying wav
for f in `cat $HMM/lists/wavlist_timit.train`; do
	formatted_wavname=`echo $f | rev | cut -d "/" -f -1,2,3 | rev | sed 's/\//_/g'`;  
        $SPH_DIR/sph2pipe -f rif $f $HMM/mfc_train/$formatted_wavname ;
done;

# for f in `cat wavlist_timit.test`;
#        formatted_wavname=`echo $f | rev | cut -d "/" -f -1,2,3 | rev | sed 's/\/_/g'`;
#        $SPH_DIR/sph2pipe -f rif $f $HMM/mfc_test/$formatted_wavname ;
# done;


#Creating WAV MFC Map

find $HMM/mfc_train/ -type f -name '*.wav' > $HMM/lists/wavlist_formatted.train
sed 's/\.wav/\.mfc/g' $HMM/lists/wavlist_formatted.train > $HMM/lists/mfclist_formatted.train
paste $HMM/lists/wavlist_formatted.train $HMM/lists/mfclist_formatted.train > $HMM/lists/map_train.scp
#find $HMM/mfc_test/ -type f -name '*.wav' > $HMM/lists/wavlist_formatted.test
#sed 's/\.wav/\.mfc/g' $HMM/lists/wavlist_formatted.test  > $HMM/lists/mfclist_formatted.test
#paste $HMM/lists/wavlist_formatted.test $HMM/lists/mfclist_formatted.test > $HMM/lists/map_test.scp

#Extracting MFCCs

HCopy -C $HMM/configs-hcopy -S $HMM/lists/map_train.scp
#HCopy -C $HMM/configs-hcopy -S $HMM/lists/map_test.scp




