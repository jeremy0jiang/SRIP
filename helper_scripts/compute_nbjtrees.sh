#!/bin/bash

# USAGE: compute_nbjtrees.sh <sequence> <inferred_tree> <threshold>
filename="${2%.*}"
echo "...."
echo $filename
echo "...."
echo "=== Generating tree ===";
echo -n "---Create distance matrix from sequence..."
python ../format.py -i $1 -o "$filename.format"
fastme -i $filename.format --dna=F84 -O "$filename.fas.matrix" -g –c
echo "$filename.format"

if [ -f $2 ] ; then
    echo "aha"
fi
rm $filename.format
rm $filename.format_fastme_stat.txt
rm $filename.format_fastme_tree.nwk
echo "done"

echo -n "---Use newick utility to remove branches..."
nw_ed $2 'i & b < '"$3"'' o > "$2.polytomy"
echo "done"

echo -n "---Neighbor join low support branch..."

if [[ $2 = *"fasttree"* ]]; then
    type="fasttree"
else
    type="raxml"
fi
python ../nbj_left_right.py -m "$filename.fas.matrix" -p "$2.polytomy" -o "$filename.$type.threshold=$3.nbj.tre"
echo {"$filename.nbj.tre"}
echo "done"
