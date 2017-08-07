#!/usr/bin/env python


import glob

type='raxml'
values = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
inf = 0.0
numbers = ["00","01","02","03","04"]
for n in numbers:
    values = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    for f in glob.iglob('../tree-simulations/param-'+n+'*/trees_inferred_'+type+'/*inf.'+type+'.stats'):
    	with open(f) as fh:
            for idx, row in enumerate(fh.readlines()[-6:]):
                values[idx] += float(row.strip().split(' ')[-1])
    
    values = [x/20 for x in values]    
    print(values)
#for f in glob.iglob('../tree-simulations/param-00*/trees_inferred_fasttree/*inferred.fasttree.tre.stats'):
    # print(f)
 #   with open(f) as fh:
  #      row = fh.readlines()[3]
#	inf += float(row.strip().split(' ')[-1])






values = [x/20 for x in values]    
#print(inf/20)
