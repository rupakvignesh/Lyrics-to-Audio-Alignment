#!/bin/tcsh

# Creates initial hmm models
# with HInit and HRest the segmentation information
# Author: Rupak Vignesh

set count=1
set num_phones=`cat $1 |wc -l`
while ($count <= $num_phones)
  set phone=`cat $1 | head -$count | tail -1` 
  HInit -m 1 -C Configs/config-init -X lab -S lists/mfclist_formatted.train -M hmm -l $phone protos/$2
  sed s/$2/$phone/ hmm/$2 > hmm/$phone
  
  HRest -m 1 -C Configs/config-init -X lab -S lists/mfclist_formatted.train -M hmm/reestimatedhmms/ -l $phone hmm/$phone
  @ count++
end

cat hmm/reestimatedhmms/* > hmm/hmmdefs

