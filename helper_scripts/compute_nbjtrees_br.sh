#!/bin/bash
# USAGE: compute_nbjtrees.sh <sequence> <inferred_tree> <threshold> <q>
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


echo -n "---Use newick utility to remove branches length shorter than q$4..."
#echo $2
#nw_ed $2 'i & b < '"$3"'' o > "$2.polytomy"
/Users/jeremyjiang/Desktop/SRIP/helper_scripts/label_short_branches.py -i $2 -t $3| nw_ed - 'i & b < 50' o > "$2.polytomy"
echo "done"




echo -n "---Resolve polytomies using my tool..."
python ../nbj_left_right.py -m "$1.matrix" -p "$2.polytomy" -o "$filename.branch<q$4.nbj.F84.tre"
python ../MP_reroot.py "$filename.branch<q$4.nbj.F84.tre"
gzip "$filename.branch<q$4.nbj.F84.tre"
echo "done"
