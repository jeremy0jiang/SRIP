#!/bin/bash
# USAGE: ./runnbj.sh
# run this in the directory containing all of the tree parameter folders
for dir in param-$(seq -w 0 4;seq -w 21 24); do
    echo "=== Working on directory $dir ==="
#for i in $(seq -w 1 20); do
    for i in {"01","02"} ; do
        # fasttree inferred tree
        sequence=$dir/indelible/$i.fas
        fasttreetree=$dir/trees_inferred_fasttree/$i.inferred.fasttree.support.tre
        raxmltree=$dir/trees_inferred_raxml/$i.inferred.raxml.support.tre

        gunzip "${sequence}.gz"
        gunzip "${fasttreetree}.gz"
        gunzip "${raxmltree}.gz"

        echo "Working on FastTree tree $i..."
        for t_fasttree in {0.8,0.9}; do
            ./../helper_scripts/compute_nbjtrees.sh $sequence $fasttreetree $t_fasttree
            echo "done"
        done

        echo -n "Working on RaxmlTree tree $i..."
        for t_raxml in {50,80,90}; do
            ./../helper_scripts/compute_nbjtrees.sh $sequence $raxmltree  $t_raxml

            echo "done"
        done


        gzip "${sequence}"
        gzip "${fasttreetree}"
        gzip "${raxmltree}"


        rm  "$fasttreetree.polytomy"
        echo "done"
    echo "${sequence}.matrix"
    rm  "${sequence}.matrix"
    done

    echo ""
done
