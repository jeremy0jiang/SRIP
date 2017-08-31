#!/usr/bin/python
#Usage:./label_low_support -i <inputree> -t <threshold>
import dendropy
import sys, getopt
#import numpy as np
import argparse
from sys import stdin
import math

sys.setrecursionlimit(10000)

def traverse(node,t):
    
    if (len(node.child_nodes()) == 0):
        return
    #print node.label
    traverse(node.child_nodes()[0],t)
    traverse(node.child_nodes()[1],t)
    if (node.child_nodes()[0].label == None and node.child_nodes()[1].label != None):
        node.label = max(node.child_nodes()[1].label,node.label)
    if (node.child_nodes()[1].label == None and node.child_nodes()[0].label != None):
        node.label = max(node.child_nodes()[0].label,node.label)
    if (node.child_nodes()[0].label != None and node.child_nodes()[1].label != None):
        node.label = max(node.child_nodes()[1].label,node.label,node.child_nodes()[0].label)
#print node.label





if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', required=True, type=argparse.FileType('r'), default=stdin,help="Input file stream")
    parser.add_argument('-t', '--threshold', help="threshold",
                        type=float)
    #parser.add_argument('-o', '--output', required=True, type=argparse.FileType('w'), default=stdin,help="Output file stream")

    args = parser.parse_args()
    tree_str = args.input.readlines()[0]
    tree = dendropy.Tree.get(data=tree_str, schema="newick")
    leafList = tree.leaf_nodes()
#    for leaf in leafList:
#        if (len(leaf.parent_node.child_nodes()) > 1 and leaf.parent_node != tree.seed_node):
#            tree.reroot_at_node(leaf.parent_node, update_bipartitions=True,suppress_unifurcations=True)
#            break

    traverse(tree.seed_node,args.threshold)

    #print len(tree.seed_node.leaf_nodes())

    print (tree.as_string(schema='newick'))

#args.output.write((tree.as_string(schema='newick')))


