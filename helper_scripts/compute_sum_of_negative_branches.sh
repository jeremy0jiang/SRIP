#!/bin/bash
# USAGE: ./../helper_scripts/runnbj.sh
# run this in the directory containing all of the tree parameter folders
#type="fasttree"
type="raxml"
for t in {1,10,20,30,40,50,60,70}; do
#for t in {"70","75","80","85","90","95"}; do
    #echo $t
#for i in $(seq -w 1 20); do
    for i in 20; do
        nw_distance -sa -mp $i.inferred.$type.support.threshold\=$t.nbj.tre |sort|awk '/^-/ {print}'| awk 'BEGIN {s=0} {s+=$1} END {print s}'
    done
done
