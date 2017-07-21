#!/bin/bash
# USAGE: compute_nbjtrees_truetree.sh <truetree> <inferred_tree> <threshold>
filename="${2%.*}"

echo "---Create distance matrix true trees..."
if [ ! -f $1.matrix ] ; then
    python ../helper_scripts/computematrix.py -i $1 -o $1.matrix
else
    printf $1.matrix" already exists\n"
fi
echo "done"


echo -n "---Use newick utility to remove branches below $3..."
echo $2
python ../MP_reroot.py $2
nw_ed $2 'i & b < '"$3"'' o > "$2.polytomy"
echo "done"




echo -n "---Neighbor join low support branch..."
python ../nbj_left_right.py -m "$1.matrix" -p "$2.polytomy" -o "$filename.threshold=$3.truetree.nbj.tre"
python ../MP_reroot.py "$filename.threshold=$3.truetree.nbj.tre"
gzip "${filename}.threshold=$3.truetree.nbj.tre"
echo "done"
