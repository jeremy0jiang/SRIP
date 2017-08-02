#!/bin/bash
# USAGE: ./../helper_scripts/runnbj.sh
# run this in the directory containing all of the tree parameter folders
for dir in param-04*; do
#for dir in param-{"02","03","04"}* ; do
    echo "=== Working on directory $dir ==="
    #for i in $(seq -w 1 20); do
    for i in 01; do
        # fasttree inferred tree
        sequence=$dir/indelible/$i.fas
        fasttreetree=$dir/trees_inferred_fasttree/$i.inferred.fasttree.support.tre
        raxmltree=$dir/trees_inferred_raxml/$i.inferred.raxml.support.tre
        echo  "${sequence}.gz"

        gunzip "${sequence}.gz"
        gunzip "${fasttreetree}.gz"
#gunzip "${raxmltree}.gz"

        echo "Working on FastTree tree $i..."
        for t_fasttree in {80,90}; do
            ./../helper_scripts/compute_nbjtrees.sh $sequence $fasttreetree $t_fasttree
            echo "done"
        done

#echo "Working on RaxmlTree tree $i..."
#        for t_raxml in {80,90}; do
#            ./../helper_scripts/compute_nbjtrees.sh $sequence $raxmltree  $t_raxml
#            echo "done"
#        done


        gzip "${sequence}"
        gzip "${fasttreetree}"
#       gzip "${raxmltree}"


        rm  "$fasttreetree.polytomy"
#       rm  "$raxmltree.polytomy"
        echo "done"
    rm  "${sequence}.matrix"
    done

    echo ""
done
