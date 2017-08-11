#!/bin/bash
# USAGE: ./../helper_scripts/runnbj.sh
# run this in the directory containing all of the tree parameter folders
#type="fasttree"
type="raxml"
#for t in {10,20,30,40,50,60,70,80,85,90,95}; do
#for t in {"70","75","80","85","90","95"}; do
    #echo $t
    for i in $(seq -w 1 20); do
#for i in {"01","02"}; do
        nw_distance -sa -mp $i.inferred.$type.support.tre | awk 'BEGIN {s=0} {s+=$1} END  {printf "%s\n",s}'
#done
#echo ''
done
