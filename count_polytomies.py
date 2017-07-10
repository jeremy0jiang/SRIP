#!/usr/bin/env python
import dendropy
import sys, getopt


def count(cur):
    sum = 0
    if(cur == None):
        return 0


    for child in cur.child_nodes():
        sum = sum + count(child)

    if (len(cur.child_nodes()) > 2):
        return sum+1
    else:
        return sum

if __name__ == '__main__':

    inputfile = sys.argv[1]
    input= open(inputfile, "r")

    tree_str = input.readlines()[0]
    #tree_str = "[&R] (((1036:0.0214651885794,1035:0.0354841403334)True:0.00275948649595,688:0.0206453098687)True:-5.00000250009e-07,654:0.0206824287469,(182:0.0696922061759,(380:0.0516417428649,362:0.0547875428611)True:0.00792656640408)True:0.0777423069287)True;"
    #tree_str ="(a,(4,(5,12,34,45,56),6,7),c,d,(e,f,g),(j,i,o,p,r));"
    tree = dendropy.Tree.get(data=tree_str, schema="newick")
    print(tree.as_ascii_plot())
    print (tree.as_string(schema='newick'))


    num_polytomies = count(tree.seed_node)
    print num_polytomies
