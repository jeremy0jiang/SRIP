#!/bin/bash
# USAGE: compute_sum_Nbranches <inferred_tree.gz>
# $234:<sequence> <inferred_tree>
t_low=0
t_high=100
inf=$1
value1=100
t=`echo "($t_low + $t_high)/2.0"|bc`
while [ $t_diff -gt 5 ];do
    gzcat $inf.gz | nw_distance -mp -sa -| sort| head -n300 > $inf.brln
    value=`../../../helper_scripts/sum_negative.py $inf.brln`
    ../../../compute_nbjtrees.sh $2 $3 $t
    if value
done
echo $value
#t_diff=$t2-$t1
