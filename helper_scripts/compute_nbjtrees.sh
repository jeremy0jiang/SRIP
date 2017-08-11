#!/bin/bash
# USAGE: compute_nbjtrees.sh <sequence> <inferred_tree> <threshold>
filename="${2%.*}"

echo "---Create distance matrix from sequence..."
if [ ! -f $1.matrix ] ; then
    python ../format.py -i $1 -o "$filename.format"
    fastme -i $filename.format -O "$1.matrix" --dna=F84 –c --gamma=5.256
    rm $filename.format
    rm $filename.format_fastme_stat.txt
    rm $filename.format_fastme_tree.nwk
else
    printf $1.matrix" already exists\n"
fi
echo "done"


echo -n "---Use newick utility to remove branches below $3..."
#echo $2
nw_ed $2 'i & b < '"$3"'' o > "$2.polytomy"
echo "done"




echo -n "---Neighbor join low support branch..."
python ../nbj_left_right.py -m "$1.matrix" -p "$2.polytomy" -o "$filename.threshold=$3.nbj.F84.tre"
python ../MP_reroot.py "$filename.threshold=$3.nbj.F84.tre"
gzip "${filename}.threshold=$3.nbj.F84.tre"
echo "done"
