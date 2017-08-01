#!/bin/bash
for dir in param-00*; do
	sum=7
	d=20 
	for i in $(seq -w 1 20); do
		sequence=$dir/indelible/$i.fas
		truetree=$dir/trees_true_simulated/$i.tre
		
		gunzip "${sequence}.gz"
		gunzip "${truetree}.gz"

		python ./../format.py -i $sequence -o $sequence.format  
		sed $sequence.format 's/>//g' >$sequence.no.format		
	        #fastme -i $sequence.no.format --dna=L -o $i.fastme.tre -g  
              
		#a=./helper_scripts/compareTrees.missingBranch $truetree $i.fastme.tre| cut -d' ' -f3	
		#sum=$sum+a
                #rm $sequence.format
		#rm $sequence.no.format
		#rm $i.fastme.tre
		gzip $sequence
		gzip $truetree


	done
	echo ($sum/10)|bc -l
	
done

