#!/bin/bash

# USAGE: generate-trees.sh <sequence> <inferred_tree> <threshold>

echo "=== Generating tree $i... ===";

echo "Create distance matrix from sequence..."
python ../format.py -i $seq -o $format
fastme -i $format --dna=F84 -O $matrix -g –c

echo "Remove branch below threshold..."
nw_ed $1 'i & b < '"$t"'' o > $1".polytomy"

echo "Resolve polytomies..."
python ../nbj_left_right.py -m $matrix -p $1".polytomy" -o $nbj

