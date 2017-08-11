#!/bin/bash
# USAGE: ./../helper_scripts/run_contract_short_branches.sh
# run this in the directory containing all of the tree parameter folders
#for dir in param-02*; do
for dir in param-{"02","03","04"}* ; do
    echo "=== Working on directory $dir ==="
    for i in $(seq -w 1 20); do
#for i in 01; do
        # fasttree inferred tree
        sequence=$dir/indelible/$i.fas
        fasttreetree=$dir/trees_inferred_fasttree/$i.inferred.fasttree.tre
        raxmltree=$dir/trees_inferred_raxml/$i.inferred.raxml.tre
        #echo  "${sequence}.gz"

        gunzip "${sequence}.gz"
        gunzip "${fasttreetree}.gz"
        gunzip "${raxmltree}.gz"

        echo "Working on FastTree tree $i..."
        f_q1=`nw_distance -sa -mp $fasttreetree| numlist -quart1`
        f_q2=`nw_distance -sa -mp $fasttreetree| numlist -med`
        f_q3=`nw_distance -sa -mp $fasttreetree| numlist -quart3`
        r_q1=`nw_distance -sa -mp $raxmltree| numlist -quart1`
        r_q2=`nw_distance -sa -mp $raxmltree| numlist -med`
        r_q3=`nw_distance -sa -mp $raxmltree| numlist -quart3`
        i=1
        for t_fasttree in {$f_q1,$f_q2,$f_q3}; do
            ./../helper_scripts/compute_nbjtrees_br.sh $sequence $fasttreetree $t_fasttree $i
            echo "done"
            let "i+=1"
        done
        i=1
        echo "Working on RaxmlTree tree $i..."
        for t_raxml in {$r_q1,$r_q2,$r_q3}; do
            ./../helper_scripts/compute_nbjtrees_br.sh $sequence $raxmltree $t_raxml $i
            echo "done"
            let "i+=1"
        done


        gzip "${sequence}"
        gzip "${fasttreetree}"
        gzip "${raxmltree}"


        rm  "$fasttreetree.polytomy"
        rm  "$raxmltree.polytomy"
        echo "done"
    rm  "${sequence}.matrix"
    done

    echo ""
done
