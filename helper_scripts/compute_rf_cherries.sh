#!/bin/bash
# USAGE: Just run this script in the directory containing all of the tree parameter folders

#for dir in param-00*; do
for dir in param-01*; do
    echo "=== Working on directory $dir ==="
    for i in 04; do
#for i in $(seq -w 1 20); do
        echo "FastTree tree $i stats"  > $dir/trees_inferred_fasttree/$i.fasttree.stats
        for t in {"80","90"}; do
            gunzip $dir/trees_true_simulated/$i.tre.gz  $dir/trees_inferred_fasttree/$i.inferred.fasttree.support.threshold=$t.nbj.tre.gz
            echo -n "Working on FastTree tree $i..."
            echo -n "Tree Error RF for threshold $t: " >> $dir/trees_inferred_fasttree/$i.fasttree.stats
            echo $(echo -n '(' && echo -n `./../helper_scripts/compareTrees.missingBranch $dir/trees_true_simulated/$i.tre $dir/trees_inferred_fasttree/$i.inferred.fasttree.support.threshold=$t.nbj.tre | cut -d' ' -f3` && echo -n ' + ' && echo -n `./../helper_scripts/compareTrees.missingBranch $dir/trees_inferred_fasttree/$i.inferred.fasttree.support.threshold=$t.nbj.tre $dir/trees_true_simulated/$i.tre | cut -d' ' -f3` && echo -n ') / 2') | bc -l >> $dir/trees_inferred_fasttree/$i.fasttree.stats
            echo -n "Number of Cherries for threshold $t: " >> $dir/trees_inferred_fasttree/$i.fasttree.stats
            ./../helper_scripts/count_cherries.sh < "$dir/trees_inferred_fasttree/$i.inferred.fasttree.support.threshold=$t.nbj.tre" >> $dir/trees_inferred_fasttree/$i.fasttree.stats
            echo " done"
	    gzip $dir/trees_true_simulated/$i.tre $dir/trees_inferred_fasttree/$i.inferred.fasttree.support.threshold=$t.nbj.tre
        done



        echo "RaxmlTree tree $i stats"  > $dir/trees_inferred_raxml/$i.raxml.stats
        for t in {"80","90"}; do
            gunzip $dir/trees_true_simulated/$i.tre.gz  $dir/trees_inferred_raxml/$i.inferred.raxml.support.threshold=$t.nbj.tre.gz
            echo -n "Working on RAxML tree $i..."
            echo -n "Tree Error RF for threshold $t: " >> $dir/trees_inferred_raxml/$i.raxml.stats
            echo $(echo -n '(' && echo -n `./../helper_scripts/compareTrees.missingBranch $dir/trees_true_simulated/$i.tre $dir/trees_inferred_raxml/$i.inferred.raxml.support.threshold=$t.nbj.tre | cut -d' ' -f3` && echo -n ' + ' && echo -n `./../helper_scripts/compareTrees.missingBranch $dir/trees_inferred_raxml/$i.inferred.raxml.support.threshold=$t.nbj.tre $dir/trees_true_simulated/$i.tre | cut -d' ' -f3` && echo -n ') / 2') | bc -l >> $dir/trees_inferred_raxml/$i.raxml.stats
            echo -n "Number of Cherries for threshold $t: " >> $dir/trees_inferred_raxml/$i.raxml.stats
            ./../helper_scripts/count_cherries.sh < "$dir/trees_inferred_raxml/$i.inferred.raxml.support.threshold=$t.nbj.tre" >> $dir/trees_inferred_raxml/$i.raxml.stats
            echo " done"
	    gzip $dir/trees_true_simulated/$i.tre $dir/trees_inferred_raxml/$i.inferred.raxml.support.threshold=$t.nbj.tre
        done
    done
    echo ""
done
