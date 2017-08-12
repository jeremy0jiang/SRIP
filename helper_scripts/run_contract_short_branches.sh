#!/bin/bash
# USAGE: ./../helper_scripts/run_contract_short_branches.sh
# run this in the directory containing all of the tree parameter folders
for dir in param-00*; do
#for dir in param-{"02","03","04"}* ; do
    echo "=== Working on directory $dir ==="
#for i in $(seq -w 1 20); do
    for i in 01; do
        # fasttree inferred tree
        sequence=$dir/indelible/$i.fas
#        fasttreetree=$dir/trees_inferred_fasttree/$i.inferred.fasttree.tre
#        raxmltree=$dir/trees_inferred_raxml/$i.inferred.raxml.tre
        fastmetree=$dir/trees_inferred_fastme/$i.inferred.fastme.f84.tre

#        gunzip "${sequence}.gz"
#        gunzip "${fasttreetree}.gz"
#        gunzip "${raxmltree}.gz"
        gunzip "${fastmetree}.gz"

        echo "Working on FastTree tree $i..."

        for t_fastme in {"0","0.0001","0.001","0.005","0.01","0.1"}; do
            /helper_scripts/compute_nbjtrees_br.sh $sequence $fastmetree $t_fastme
            echo "done"
        done

        echo "Working on FastTree tree $i..."



        gzip "${sequence}"
        gzip "${fastmetree}"


        rm  "$fastmetree.polytomy"
        echo "done"
    rm  "${sequence}.matrix"
    done

    echo ""
done
