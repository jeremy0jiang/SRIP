#!/bin/bash
# USAGE: compute_nbjtrees.sh <sequence> <inferred_tree> <threshold>
filename="${2%.*}"

echo "---Create distance matrix from sequence..."
if [ ! -f $1.matrix ] ; then
    python ../format.py -i $1 -o "$1.format"
    fastme -i $1.format -O "$1.matrix" --dna=F84 –c --gamma=5.256
    rm $1.format
    rm $1.format_fastme_stat.txt
    rm $1.format_fastme_tree.nwk
else
    printf $1.matrix" already exists\n"
fi
echo "done"


echo -n "---Use newick utility to remove branches length shorter than $3 ..."
#echo $2
#nw_ed $2 'i & b < '"$3"'' o > "$2.polytomy"
../helper_scripts/label_short_branches.py -i $2 -t $3| nw_ed - 'i & b < 50' o > "$2.$3.polytomy"
echo "done"




echo -n "---Resolve polytomies using my tool..."
python ../nbj_average.py -m "$1.matrix" -p "$2.$3.polytomy" -o "$filename.branch<$3.nbj.tre.new"
#python ../MP_reroot.py "$filename.branch<$3.nbj.tre"
#rm "$2.polytomy"
#gzip "$filename.branch<$3.nbj.tre"
echo "done"
