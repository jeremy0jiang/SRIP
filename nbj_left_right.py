#!/usr/bin/python

'''
Shenghao Jiang 2017

Resolve polytomies by neighbor joining 

'''

# imports
import dendropy
import sys, getopt
import numpy as np
import argparse
from sys import stdin

sys.setrecursionlimit(10000)


# recursively join nodes in the tree
def nbj(cur):
    # when cur is leaf
    if cur.is_leaf():
        return

    childList = cur.child_nodes()

    # when cur is polytomy
    if (len(childList) > 2):
        parent = cur.parent_node
        grandparent = parent.parent_node

        if (grandparent != None):
            grandparent.remove_child(parent)
            parent_length = parent.edge_length

        parent.remove_child(cur)
        combineList = list()
        combineList.append(parent)
        combineList += childList
        subtree = combine(combineList)
        #subtree.print_plot()

        if (grandparent != None):
            parent.edge_length = parent_length
            grandparent.add_child(parent)
        else:
            tree.seed_node = parent

    # recursively join children
    for child in childList:
        nbj(child)
    return


# given a nodelist, use neighbor joining to combine these nodes
def combine(nodeList):
    # the parent node of cur
    subroot = nodeList[0]

    numOfNode = len(nodeList)

    # get distance matrix from creat_matrix method
    smallMatrix = create_matrix(nodeList)

    # create Q-matrix
    QMatrix = np.empty([numOfNode, numOfNode])
    QMatrix[:] = float("inf")
    for i in range(0, numOfNode):
        for j in range(i + 1, numOfNode):
            QMatrix[i][j] = (numOfNode - 2) * smallMatrix[i][j] - smallMatrix[i, :].sum() - smallMatrix[:, j].sum()

    # select min column and min row
    minRow, minColumn = np.unravel_index(QMatrix.argmin(), QMatrix.shape)
    node_a = nodeList[minRow]
    node_b = nodeList[minColumn]

    # compute distance from the pair memebers to the new node
    dist_au = 0.5 * smallMatrix[minRow][minColumn] + 0.5 / (numOfNode - 2) * (
        smallMatrix[minRow, :].sum() - smallMatrix[:, minColumn].sum())
    dist_bu = 0.5 * smallMatrix[minRow][minColumn] - 0.5 / (numOfNode - 2) * (
        smallMatrix[minRow, :].sum() - smallMatrix[:, minColumn].sum())

    # join pair members
    ch1 = dendropy.Node()
    node_a.edge_length = dist_au
    node_b.edge_length = dist_bu
    ch1.add_child(node_a)
    ch1.add_child(node_b)

    # distance from other node from the new node
    dist_uk = np.empty(numOfNode)
    for i in range(0, numOfNode):
        dist_uk[i] = 0.5 * (smallMatrix[minRow][i] + smallMatrix[minColumn][i] - smallMatrix[minRow][minColumn])

    # remove used distance from distance matrix
    dist_uk = np.delete(dist_uk, minRow)
    dist_uk = np.delete(dist_uk, minColumn - 1)
    smallMatrix = np.delete(smallMatrix, minRow, axis=0)
    smallMatrix = np.delete(smallMatrix, minColumn - 1, axis=0)
    smallMatrix = np.delete(smallMatrix, minRow, axis=1)
    smallMatrix = np.delete(smallMatrix, minColumn - 1, axis=1)
    nodeList.remove(node_a)
    nodeList.remove(node_b)

    numOfNode -= 2

    # iteratively
    while numOfNode > 1:
        dist_tocompare = np.empty(numOfNode)

        # compare Q-matrix value
        for taxa in range(0, numOfNode):
            dist_tocompare[taxa] = (numOfNode - 1) * dist_uk[taxa] - smallMatrix[:, taxa].sum()-dist_uk[taxa]
        closestTaxa = dist_tocompare.argmin()
        closestNode = nodeList[closestTaxa]

        # distacne from closest node to the center
        dist_au = 0.5 * dist_uk[closestTaxa] + 0.5 / (numOfNode - 1) * (
            smallMatrix[closestTaxa, :].sum() - dist_uk.sum() + dist_uk[closestTaxa])
        dist_uu = 0.5 * dist_uk[closestTaxa] - 0.5 / (numOfNode - 1) * (
            smallMatrix[closestTaxa, :].sum() - dist_uk.sum() + dist_uk[closestTaxa])

        # join the closest nide
        ch2 = dendropy.Node()
        ch1.edge_length = dist_uu
        closestNode.edge_length = dist_au
        ch2.add_child(ch1)
        ch2.add_child(closestNode)
        # distance from other nodes to the center
        dist_ab = dist_uk[closestTaxa]
        for taxa in range(0, numOfNode):
            dist_uk[taxa] = 0.5 * (dist_uk[taxa] + smallMatrix[closestTaxa][taxa] - dist_ab)
        dist_uk = np.delete(dist_uk, closestTaxa)

        # delete used distance from distance matrix
        smallMatrix = np.delete(smallMatrix, closestTaxa, axis=0)
        smallMatrix = np.delete(smallMatrix, closestTaxa, axis=1)

        # remove the node from nodelist
        nodeList.remove(closestNode)
        numOfNode -= 1

        # set old center to the new center
        ch1 = ch2


    # join the left node from node list
    nodeList[0].edge_length = dist_uk[0]
    ch1.add_child(nodeList[0])

    # create a ladderlike tree
    laddertree = dendropy.Tree()
    laddertree.seed_node = ch1

    # update taxon
    laddertree.update_taxon_namespace()
    laddertree.is_rooted = True


    # reroot on the parent node to stick the ladderlike tree to the original tree
    laddertree.reroot_at_node(subroot, update_bipartitions=True, suppress_unifurcations=False)

    return laddertree


# find the two closest leaves whose mrca is the node
def find_two_closest(root):
    # closest leaves to each child of the root
    closestList = list()

    # select the cloest leaf to each child
    for child in root.child_nodes():
        minDist = [None, float("inf")]
        find_closest_leaf(child, 0, minDist)
        closestList.append(minDist[0])

    # select two closest leaves among these leaves
    numOfChild = len(root.child_nodes())
    pairwiseMatrix = np.empty([numOfChild, numOfChild])
    pairwiseMatrix[:] = float("inf")
    for i in range(0, numOfChild):
        for j in range(i + 1, numOfChild):
            pairwiseMatrix[i][j] = Matrix[taxa_dictionary[closestList[i]]][taxa_dictionary[closestList[j]]]

    # select min column and min row
    minRow, minColumn = np.unravel_index(pairwiseMatrix.argmin(), pairwiseMatrix.shape)
    leaf_a = closestList[minRow]
    leaf_b = closestList[minColumn]

    return leaf_a,leaf_b


# find the closest leaf to a certain node
def find_closest_leaf(cur,dist_to_subroot,minDist):
    # when cur is none
    if cur == None:
        return
    # when cur is leaf
    if cur.is_leaf():
        if dist_to_subroot < minDist[1]:
            minDist[0] = cur
            minDist[1] = dist_to_subroot
        return
    # when cur is a internal node
    for child in cur.child_nodes():
        if (dist_to_subroot + child.edge_length < minDist[1]):
            find_closest_leaf(child, dist_to_subroot + child.edge_length,minDist)


# create distance matrix based on a left-side leaf and a right-side leaf on two nodes
def create_matrix(nodeList):
    # create a left-side leaf list and a right-side leaf lise
    leftList = nodeList[:]
    rightList = nodeList[:]


    # populate the left-side and right-side leaf list

    leftList[0] = tree.seed_node
    if nodeList[0] == tree.seed_node:
        rightList[0] = tree.seed_node
    else:
        rightList[0] = nodeList[0].leaf_nodes()[0]



    for index in range(1, len(nodeList)):
        cur = nodeList[index]
        if len(cur.child_nodes()) == 0:
            leftList[index] = cur
            rightList[index] = cur
        else:
            #leftList[index], rightList[index] = cur.child_nodes()[0].leaf_nodes()[0],cur.child_nodes()[1].leaf_nodes()[0]
            leftList[index], rightList[index] = find_two_closest(cur)

    numOfNode = len(nodeList)

    # create the distance matrix
    smallMatrix = np.empty([numOfNode, numOfNode])
    i = j = 0

    for i in range(0, numOfNode):
        i_left = leftList[i]
        i_right = rightList[i]
        for j in range(0, numOfNode):
            j_left = leftList[j]
            j_right = rightList[j]
            smallMatrix[i][j] = 0.5 * (
            Matrix[taxa_dictionary[i_left]][taxa_dictionary[j_right]] + Matrix[taxa_dictionary[i_right]][
                taxa_dictionary[j_left]] - Matrix[taxa_dictionary[i_left]][taxa_dictionary[i_right]] -
            Matrix[taxa_dictionary[j_left]][taxa_dictionary[j_right]])


    #print smallMatrix
    return smallMatrix

# if code is executed (and not imported)
if __name__ == '__main__':
    # parse args
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-m', '--inputmatrix', required=True, type=argparse.FileType('r'), default=stdin,
                        help="Input matrix file stream")
    parser.add_argument('-p', '--inputpolytomy', required=True, type=argparse.FileType('r'), default=stdin,
                        help="Input polytomy file stream")
    parser.add_argument('-o', '--output', required=True, type=argparse.FileType('w'), default=stdin,
                        help="Output file stream")
    args = parser.parse_args()

    lines = args.inputmatrix.readlines()

    # number of taxa
    num_taxa = int(lines[0])

    taxaName = []
    Matrix = np.zeros((num_taxa, num_taxa))

    # create distance matrix from input matrix file
    for lineNumber in range(1, num_taxa + 1):
        line = lines[lineNumber].split()
        taxaName.append(line[0][1:])
        for wordNumber in range(1, num_taxa + 1):
#            if line[wordNumber] == "NA":
#                Matrix[lineNumber - 1][wordNumber - 1] = 5.0
#            else:
            Matrix[lineNumber - 1][wordNumber - 1] = float(line[wordNumber])
            wordNumber = +1
        lineNumber = +1

    # build the polytomy tree from input tree file
    tree_str = args.inputpolytomy.readlines()[0]
    tree = dendropy.Tree.get(data=tree_str, schema="newick")



    # create leaf list
    leafList = tree.leaf_nodes()

    # create a node name to matrix dictionary
    taxa_dictionary = dict()  # taxadictionary


    for i in range(0, num_taxa):
        for node in leafList:
            if (taxaName[i] == node.taxon.label):
                taxa_dictionary[node] = i
    tree.is_rooted = False


    # reroot on an internal node
    for leaf in leafList:
        if (len(leaf.parent_node.child_nodes()) > 1 and leaf.parent_node != tree.seed_node):
            tree.reroot_at_node(leaf.parent_node, update_bipartitions=True, suppress_unifurcations=True)
            break

    # reroot on a random leaf
    tree.reroot_at_node(tree.seed_node.leaf_nodes()[0], update_bipartitions=True, suppress_unifurcations=False)
    #print tree.seed_node
    #tree.print_plot()
    # apply neighbor joining
    nbj(tree.seed_node)
    #tree.print_plot()
    # reroot at the child of the root
    tree.reroot_at_node(tree.seed_node.child_nodes()[0],update_bipartitions=True, suppress_unifurcations=False)

    # output tree in newick format
    args.output.write((tree.as_string(schema='newick'))[5:])
    #print tree.as_string(schema='newick')
    # close files
    args.inputpolytomy.close()
    args.inputmatrix.close()
    args.output.close()
