#!/bin/bash
# USAGE: Just run this script in the directory containing all of the tree parameter folders

for dir in param-{"00","xxx"}*; do
    echo "=== Working on directory $dir ==="
    for i in $(seq -w 1 2); do
        for t in {"0.8","0.9"}; do

            # fasttree inferred tree
            echo -n "Working on FastTree tree $i..."
            echo -n "Tree Error RF for threshold $t : " >> $dir/trees_inferred_fasttree/$i.inferred.fasttree.tre.stats
            echo $(echo -n '(' && echo -n `./../helper_scripts/compareTrees.missingBranch $dir/trees_true_simulated/$i.tre $dir/trees_inferred_fasttree/$i.inferred.fasttree.support.threshold=$t.nbj.tre | cut -d' ' -f3` && echo -n ' + ' && echo -n `./../helper_scripts/compareTrees.missingBranch $dir/trees_inferred_fasttree/$i.inferred.fasttree.support.threshold=$t.nbj.tre $dir/trees_true_simulated/$i.tre | cut -d' ' -f3` && echo -n ') / 2') | bc -l >> $dir/trees_inferred_fasttree/$i.inferred.fasttree.tre.stats
            echo -n "Number of Cherries for threshold $t : " >> $dir/trees_inferred_fasttree/$i.inferred.fasttree.tre.stats
            ./../helper_scripts/count_cherries.sh < "$dir/trees_inferred_fasttree/$i.inferred.fasttree.support.threshold=$t.nbj.tre" >> $dir/trees_inferred_fasttree/$i.inferred.fasttree.tre.stats
            echo " done"

        done

#            # raxml inferred tree
#            echo -n "Working on RAxML tree $i..."
#            echo -n "Tree Error RF = (FN+FP)/2: " >> $dir/trees_inferred_raxml/$i.inferred.raxml.tre.stats
#            echo $(echo -n '(' && echo -n `compareTrees.missingBranch $dir/trees_true_simulated/$i.tre $dir/trees_inferred_raxml/$i.inferred.raxml.tre | cut -d' ' -f3` && echo -n ' + ' && echo -n `compareTrees.missingBranch $dir/trees_inferred_raxml/$i.inferred.raxml.tre $dir/trees_true_simulated/$i.tre | cut -d' ' -f3` && echo -n ') / 2') | bc -l >> $dir/trees_inferred_raxml/$i.inferred.raxml.tre.stats
#            echo " done"

        done
    echo ""
done
