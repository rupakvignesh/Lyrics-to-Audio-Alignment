#!/bin/tcsh

# Creates initial hmm models
# with HInit and HRest the segmentation information
# Args: phonelist, proto_file
# Author: Rupak Vignesh

set count=1
set num_phones=`cat $1 |wc -l`
while ($count <= $num_phones)
  set phone=`cat $1 | head -$count | tail -1` 
  HInit -m 1 -C Configs/config-init -X lab -S lists/train.male.mfclist -M male_models/hmm -l $phone protos/$2
  sed s/$2/$phone/ male_models/hmm/$2 > male_models/hmm/$phone
  
  HRest -m 1 -C Configs/config-init -X lab -S lists/train.male.mfclist -M male_models/hmm/reestimatedhmms/ -l $phone male_models/hmm/$phone
  @ count++
end

cat male_models/hmm/reestimatedhmms/* > male_models/hmm/hmmdefs

