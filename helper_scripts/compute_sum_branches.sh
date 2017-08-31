#!/bin/bash
# USAGE: ./../helper_scripts/compute_sum_branches.sh
# run this in the directory containing all of the tree parameter folders
#type="fasttree"
#type="raxml"
type="fastme"
for t in {0,0.0001,0.001,0.005,0.01,0.1}; do
#for t in {10,20,30,40,50,60,70,80,85,90,95}; do
    #echo $t
for i in $(seq -w 1 20); do
#for i in 01; do
    nw_distance -sa -mp $i.inferred.fastme.f84.tre |numlist -abs|numlist -sum
#done
#echo ''
done
echo ''
