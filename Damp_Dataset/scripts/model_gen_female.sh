#!/bin/tcsh

# Creates initial hmm models
# with HInit and HRest the segmentation information
# Args: phonelist, proto_file
# Author: Rupak Vignesh

set count=1
set num_phones=`cat $1 |wc -l`
while ($count <= $num_phones)
  set phone=`cat $1 | head -$count | tail -1` 
  HInit -m 1 -C Configs/config-init -X lab -S lists/train.female.mfclist -M female_models/hmm -l $phone protos/$2
  sed s/$2/$phone/ female_models/hmm/$2 > female_models/hmm/$phone
  
  HRest -m 1 -C Configs/config-init -X lab -S lists/train.female.mfclist -M female_models/hmm/reestimatedhmms/ -l $phone female_models/hmm/$phone
  @ count++
end

cat hmm/reestimatedhmms/* > hmm/hmmdefs

