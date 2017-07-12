#!/bin/bash

# USAGE: generate-trees.sh <sequence> <inferred_tree> <threshold>

filename="${1%.*}"

echo "=== Generating tree ===";

echo "Create distance matrix from sequence..."
python ../format.py -i $1 -o $filename.format
fastme -i $filename.format --dna=F84 -O $filename.fas.matrix -g –c
rm $filename.format
rm $filename.format_fastme_stat.txt
rm $filename.format_fastme_tree.nwk
echo "done"

echo "Use newick utility to remove branches..."
nw_ed $2 'i & b < '"$3"'' o > $2.polytomy
echo "done"

echo "Neighbor join low support branch..."
python ../nbj_left_right.py -m $filename.fas.matrix -p $2.polytomy -o $filename.nbj.tre
echo "done"
