#!/bin/bash
# USAGE: ./../helper_scripts/runnbj.sh
# run this in the directory containing all of the tree parameter folders
for dir in param-00*; do
#for dir in param-{"00","01","02","03","04"}* ; do
    echo "=== Working on directory $dir ==="
#for i in $(seq -w 1 20); do
    for i in 20; do
        # fasttree inferred tree
        sequence=$dir/indelible/$i.fas
        fasttreetree=$dir/trees_inferred_fasttree/$i.inferred.fasttree.support.tre
#raxmltree=$dir/trees_inferred_raxml/$i.inferred.raxml.support.tre
        fastmetree=$dir/trees_inferred_fastme/$i.inferred.fastme.support.tre
        #echo  "${sequence}.gz"

        gunzip "${sequence}.gz"
        gunzip "${fasttreetree}.gz"
#gunzip "${raxmltree}.gz"
#gunzip "${fastmetree}.gz"

         echo "Working on FastTree tree $i..."
         for t_fasttree in 80; do
             ./../helper_scripts/compute_nbjtrees.sh $sequence $fasttreetree $t_fasttree
             echo "done"
         done
#
#        echo "Working on RaxmlTree tree $i..."
#        for t_raxml in {10,20,30,40,50,60,70,80,85,90,95}; do
#            ./../helper_scripts/compute_nbjtrees.sh $sequence $raxmltree  $t_raxml
#            echo "done"
#        done

#        echo "Working on Fastme tree $i..."
#        for t_fastme in {1,10,20,30,40,50,60,70,80,85,90,95}; do
#            ./../helper_scripts/compute_nbjtrees.sh $sequence $fastmetree $t_fastme
#            echo "done"
#        done



        gzip "${sequence}"
#        gzip "${fasttreetree}"
#        gzip "${raxmltree}"
#       gzip "${fastmetree}"

        rm  "$fasttreetree.polytomy"
#        rm  "$raxmltree.polytomy"
#       rm "$fastmetree.polytomy"
        echo "done"
#rm  "${sequence}.matrix"
    done

    echo ""
done
