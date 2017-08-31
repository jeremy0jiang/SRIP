#!/bin/bash
# USAGE: ./../helper_scripts/runnbj.sh
# run this in the directory containing all of the tree parameter folders
#type="fasttree"
type="fastme"
#for t in {"1","2","3"}; do
#for t in {"1","2","3"}; do
for t in {0,0.0001,0.001,0.005,0.01,0.1}; do
#echo $t
    for i in $(seq -w 1 20); do
#for i in 01; do    #for i in {"01","02"}; do
        nw_distance -sa -mp $i.inferred.fastme.f84.branch\<$t.nbj.tre |awk '/^-/ {print}'| awk 'BEGIN {s=0} {s+=$1} END  {printf "%s,",s}'
    done
    echo ''
done
echo ''
