#!/bin/bash
# USAGE: ./../helper_scripts/runnbj.sh
# run this in the directory containing all of the tree parameter folders
for dir in param-01*; do
#for dir in param-{"00","01","02","03","04"}* ; do
    echo "=== Working on directory $dir ==="
#for i in $(seq -w 1 20); do
    for i in 01; do
        # fasttree inferred tree
        truetree=$dir/trees_true_simulated/$i.tre
        #truetree=$dir/trees_inferred_fasttree/$i.inferred.fasttree.tre
        fasttreetree=$dir/trees_inferred_fasttree/$i.inferred.fasttree.support.tre
        raxmltree=$dir/trees_inferred_raxml/$i.inferred.raxml.support.tre
        echo  "${truetree}.gz"

        gunzip "${truetree}.gz"
        gunzip "${fasttreetree}.gz"
        gunzip "${raxmltree}.gz"

        echo "Working on FastTree tree $i..."
        for t_fasttree in {80,90}; do
            ./../helper_scripts/compute_nbjtrees_truetree.sh $truetree $fasttreetree $t_fasttree
            echo "done"
        done

         echo "Working on RaxmlTree tree $i..."
         for t_raxml in {80,90}; do
             ./../helper_scripts/compute_nbjtrees_truetree.sh $truetree $raxmltree  $t_raxml

             echo "done"
         done


        gzip "${truetree}"
        gzip "${fasttreetree}"
        gzip "${raxmltree}"


        rm  "$fasttreetree.polytomy"
    	rm  "$raxmltree.polytomy"
        echo "done"
    rm  "${truetree}.matrix"
    done

    echo ""
done
