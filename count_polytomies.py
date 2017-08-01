#!/usr/bin/env python
'''
Shenghao Jiang 2017

This program counts the number of polytomies in the tree
'''
#USAGE: python count_polytomies <polytomy_file>

import dendropy
import sys, getopt

sys.setrecursionlimit(10000)

def count(cur):
    sum = 0
    if(cur == None):
        return 0


    for child in cur.child_nodes():
        sum = sum + count(child)

    if (len(cur.child_nodes()) > 2):
        #print cur.label
        return sum+1
    else:
        return sum

if __name__ == '__main__':

    inputfile = sys.argv[1]
    input= open(inputfile, "r")

    tree_str = input.readlines()[0]
    tree = dendropy.Tree.get(data=tree_str, schema="newick")

    num_polytomies = count(tree.seed_node)
    print num_polytomies
