#!/bin/bash
# USAGE: Just run this script in the directory containing all of the tree parameter folders

for dir in param-{"00","xxx"}*; do
    echo "=== Working on directory $dir ==="
    for i in $(seq -w 1 2); do
        for t in {"80","90"}; do

            # fasttree inferred tree
            echo -n "Working on FastTree tree $i..."
            echo -n "Tree Error RF for threshold $t : " >> $dir/trees_inferred_fasttree/$i.inferred.fasttree.tre.stats
            echo $(echo -n '(' && echo -n `./../helper_scripts/compareTrees.missingBranch $dir/trees_true_simulated/$i.tre $dir/trees_inferred_fasttree/$i.inferred.fasttree.support.threshold=$t.nbj.tre | cut -d' ' -f3` && echo -n ' + ' && echo -n `./../helper_scripts/compareTrees.missingBranch $dir/trees_inferred_fasttree/$i.inferred.fasttree.support.threshold=$t.nbj.tre $dir/trees_true_simulated/$i.tre | cut -d' ' -f3` && echo -n ') / 2') | bc -l >> $dir/trees_inferred_fasttree/$i.inferred.fasttree.tre.stats
            echo -n "Number of Cherries for threshold $t : " >> $dir/trees_inferred_fasttree/$i.inferred.fasttree.tre.stats
            ./../helper_scripts/count_cherries.sh < "$dir/trees_inferred_fasttree/$i.inferred.fasttree.support.threshold=$t.nbj.tre" >> $dir/trees_inferred_fasttree/$i.inferred.fasttree.tre.stats
            echo " done"

        done
#        for t in {"80","90"}; do
#            # raxml inferred tree
#            echo -n "Working on RAxML tree $i..."
#            echo -n "Tree Error for threshold $t : " >> $dir/trees_inferred_raxml/$i.inferred.raxml.tre.stats
#            echo $(echo -n '(' && echo -n `./../helper_scripts/compareTrees.missingBranch $dir/trees_true_simulated/$i.tre $dir/trees_inferred_raxml/$i.inferred.raxml.support.threshold=$t.nbj.tre | cut -d' ' -f3` && echo -n ' + ' && echo -n `./../helper_scripts/compareTrees.missingBranch $dir/trees_inferred_raxml/$i.inferred.raxml.support.threshold=$t.nbj.tre $dir/trees_true_simulated/$i.tre | cut -d' ' -f3` && echo -n ') / 2') | bc -l >> $dir/trees_inferred_raxml/$i.inferred.raxml.tre.stats
#            echo -n "Number of Cherries for threshold $t : " >> $dir/trees_inferred_raxml/$i.inferred.raxml.tre.stats
#            ./../helper_scripts/count_cherries.sh < "$dir/trees_inferred_raxml/$i.inferred.raxml.support.threshold=$t.nbj.tre" >> $dir/trees_inferred_raxml/$i.inferred.raxml.tre.stats
#            echo " done"
#        done
    done
    echo ""
done
