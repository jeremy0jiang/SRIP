#!/usr/bin/python
#Usage:./label_short_branches -i <inputree> -t <threshold>
import dendropy
import sys, getopt
#import numpy as np
import argparse
from sys import stdin
import math

sys.setrecursionlimit(10000)

def traverse(node,t):
    if node == None:
        return
    for nd in node.child_nodes():
        traverse(nd,t)
    if (node.edge_length == None):
        l = 1000
    else:
        l = node.edge_length
    if l >= t:
        node.label = 100
    else:
        node.label = 1
#print node.edge_length, node.label


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', required=True, type=argparse.FileType('r'), default=stdin,help="Input file stream")
    parser.add_argument('-t', '--threshold', help="threshold",
                        type=float)
    #parser.add_argument('-o', '--output', required=True, type=argparse.FileType('w'), default=stdin,help="Output file stream")

    args = parser.parse_args()
    tree_str = args.input.readlines()[0]
    tree = dendropy.Tree.get(data=tree_str, schema="newick")

    traverse(tree.seed_node,args.threshold)
    print (tree.as_string(schema='newick'))

#args.output.write((tree.as_string(schema='newick')))


