#!/bin/tcsh
#Calculates duration of wavfiles in a folder
#Author: Rupak Vignesh

set count = `ls *.wav |wc -l`
set iter = 1

echo $count
set sum = 0
while($iter <= $count)
  set filename = `ls *.wav | head -$iter | tail -1`
  echo $filename
  set dur = `soxi -D $filename`
  set sum = `expr "$sum + $dur" |bc`
  @ iter++
end

echo $sum
