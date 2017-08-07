#!/bin/bash
# USAGE: Just run this script in the directory containing all of the tree parameter folders

for dir in param-{"00","01","02","03","04"}*; do
#for dir in param-04*; do
    echo "=== Working on directory $dir ==="
#for i in 01; do
    for i in $(seq -w 1 20); do
        echo "FastTree tree $i stats"  > $dir/trees_inferred_fasttree/$i.inf.fasttree.stats
        for t in {"50","80","90"}; do


            gunzip $dir/trees_true_simulated/$i.tre.gz  $dir/trees_inferred_fasttree/$i.inferred.fasttree.support.threshold=$t.inf.nbj.tre.gz
            echo -n "Working on FastTree tree $i..."
            echo -n "Tree Error RF based on inferred fasttree distance for threshold $t: " >> $dir/trees_inferred_fasttree/$i.inf.fasttree.stats
            echo $(echo -n '(' && echo -n `./../helper_scripts/compareTrees.missingBranch $dir/trees_true_simulated/$i.tre $dir/trees_inferred_fasttree/$i.inferred.fasttree.support.threshold=$t.inf.nbj.tre | cut -d' ' -f3` && echo -n ' + ' && echo -n `./../helper_scripts/compareTrees.missingBranch $dir/trees_inferred_fasttree/$i.inferred.fasttree.support.threshold=$t.inf.nbj.tre $dir/trees_true_simulated/$i.tre | cut -d' ' -f3` && echo -n ') / 2') | bc -l >> $dir/trees_inferred_fasttree/$i.inf.fasttree.stats
            echo -n "Number of Cherries for threshold $t: " >> $dir/trees_inferred_fasttree/$i.inferred.fasttree.tre.stats
            ./../helper_scripts/count_cherries.sh < "$dir/trees_inferred_fasttree/$i.inferred.fasttree.support.threshold=$t.inf.nbj.tre" >> $dir/trees_inferred_fasttree/$i.inf.fasttree.stats
            echo " done"
	    gzip $dir/trees_true_simulated/$i.tre $dir/trees_inferred_fasttree/$i.inferred.fasttree.support.threshold=$t.inf.nbj.tre

        done


        echo "RaxmlTree tree $i stats"  > $dir/trees_inferred_raxml/$i.inf.raxml.stats
        for t in {"50","80","90"}; do
            gunzip $dir/trees_true_simulated/$i.tre.gz  $dir/trees_inferred_raxml/$i.inferred.raxml.support.threshold=$t.inf.nbj.tre.gz
            echo -n "Working on RAxML tree $i..."
            echo -n "Tree Error RF based on inferred raxml distance for threshold $t: " >> $dir/trees_inferred_raxml/$i.inf.raxml.stats
            echo $(echo -n '(' && echo -n `./../helper_scripts/compareTrees.missingBranch $dir/trees_true_simulated/$i.tre $dir/trees_inferred_raxml/$i.inferred.raxml.support.threshold=$t.inf.nbj.tre | cut -d' ' -f3` && echo -n ' + ' && echo -n `./../helper_scripts/compareTrees.missingBranch $dir/trees_inferred_raxml/$i.inferred.raxml.support.threshold=$t.inf.nbj.tre $dir/trees_true_simulated/$i.tre | cut -d' ' -f3` && echo -n ') / 2') | bc -l >> $dir/trees_inferred_raxml/$i.inf.raxml.stats
            echo -n "Number of Cherries for threshold $t: " >> $dir/trees_inferred_raxml/$i.inferred.raxml.tre.stats
            ./../helper_scripts/count_cherries.sh < "$dir/trees_inferred_raxml/$i.inferred.raxml.support.threshold=$t.inf.nbj.tre" >> $dir/trees_inferred_raxml/$i.inf.raxml.stats
            echo " done"
	    gzip $dir/trees_true_simulated/$i.tre $dir/trees_inferred_raxml/$i.inferred.raxml.support.threshold=$t.inf.nbj.tre

        done
    done
    echo ""
done
