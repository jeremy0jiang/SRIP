#!/usr/bin/python
import dendropy
import sys, getopt
import numpy as np
from sets import Set
from collections import defaultdict

sys.setrecursionlimit(10000)


def nbj(cur):
    # if (len(tree.leaf_nodes()) != 1000):
    #    print len(tree.leaf_nodes())
    #    sys.exit()
    print "nbj:"
    print "current:", cur
    print tree.seed_node, "------------------------"

    if cur.is_leaf():
        print "cur is leaf"
        return

    childList = cur.child_nodes()
    print "cur child len", len(cur.child_nodes())
    print "cur child: ", childList
    print(tree.as_ascii_plot())

    #when cur is the root
    if (len(childList) > 2):

        parent = cur.parent_node
        #grandparent = parent.parent_node
        print "parent: ",parent


        parent_length = parent.edge_length
        parent.remove_child(cur)



        combineList=list()
        combineList.append(parent)
        combineList += childList
        subtree = combine(combineList)
        print "subtree:"
        print (subtree.as_ascii_plot())
        print "tree here:"
        print (tree.as_ascii_plot())
        print tree.as_string(schema='newick')
        
        for child in parent.child_nodes():
            nbj(child)
        return

    else:
        for child in childList:
            nbj(child)
        return


def combine(nodeList):
    subroot = nodeList[0]
    numOfNode = len(nodeList)
    smallMatrix = create_matrix(nodeList)

    QMatrix = np.empty([numOfNode, numOfNode])
    QMatrix[:] = float("inf")

    for i in range(0, numOfNode):
        for j in range(i + 1, numOfNode):
            QMatrix[i][j] = (numOfNode - 2) * smallMatrix[i][j] - smallMatrix[i, :].sum() - smallMatrix[:, j].sum()

    minRow, minColumn = np.unravel_index(QMatrix.argmin(), QMatrix.shape)
    node_a = nodeList[minRow]
    node_b = nodeList[minColumn]

    dist_au = 0.5 * smallMatrix[minRow][minColumn] + 0.5 / (numOfNode - 2) * (
    smallMatrix[minRow, :].sum() - smallMatrix[:, minColumn].sum())
    dist_bu = 0.5 * smallMatrix[minRow][minColumn] - 0.5 / (numOfNode - 2) * (
    smallMatrix[minRow, :].sum() - smallMatrix[:, minColumn].sum())

    ch1 = dendropy.Node()

    node_a.edge_length = dist_au
    node_b.edge_length = dist_bu
    ch1.add_child(node_a)
    ch1.add_child(node_b)

    # distance from other nodes to cluster
    dist_uk = np.empty(numOfNode)
    for i in range(0, numOfNode):
        dist_uk[i] = 0.5 * (smallMatrix[minRow][i] + smallMatrix[minColumn][i] - smallMatrix[minRow][minColumn])

    dist_uk = np.delete(dist_uk, minRow)
    dist_uk = np.delete(dist_uk, minColumn - 1)

    smallMatrix = np.delete(smallMatrix, minRow, axis=0)
    smallMatrix = np.delete(smallMatrix, minColumn - 1, axis=0)
    smallMatrix = np.delete(smallMatrix, minRow, axis=1)
    smallMatrix = np.delete(smallMatrix, minColumn - 1, axis=1)
    nodeList.remove(node_a)
    nodeList.remove(node_b)

    numOfNode -= 2

    while numOfNode > 1:
        dist_tocompare = np.empty(numOfNode)

        # compare Qmatrix value
        for taxa in range(0, numOfNode):
            dist_tocompare[taxa] = (numOfNode - 1) * dist_uk[taxa] - smallMatrix[:, taxa].sum()
        closestTaxa = dist_tocompare.argmin()
        closestNode = nodeList[closestTaxa]

        # distacne from closest node to center
        dist_au = 0.5 * dist_uk[closestTaxa] + 0.5 / (numOfNode - 1) * (
        smallMatrix[closestTaxa, :].sum() - dist_uk.sum() + dist_uk[closestTaxa])
        dist_uu = 0.5 * dist_uk[closestTaxa] - 0.5 / (numOfNode - 1) * (
        smallMatrix[closestTaxa, :].sum() - dist_uk.sum() + dist_uk[closestTaxa])

        ch2 = dendropy.Node()
        ch1.edge_length = dist_uu
        closestNode.edge_length = dist_au
        ch2.add_child(ch1)
        ch2.add_child(closestNode)

        # distance from other nodes to cluster
        dist_ab = dist_uk[closestTaxa]
        for taxa in range(0, numOfNode):
            dist_uk[taxa] = 0.5 * (dist_uk[taxa] + smallMatrix[closestTaxa][taxa] - dist_ab)
        dist_uk = np.delete(dist_uk, closestTaxa)

        # delete to form new dist matrix
        smallMatrix = np.delete(smallMatrix, closestTaxa, axis=0)
        smallMatrix = np.delete(smallMatrix, closestTaxa, axis=1)

        nodeList.remove(closestNode)
        numOfNode -= 1
        ch1 = ch2
    nodeList[0].edge_length = dist_uk[0]
    ch1.add_child(nodeList[0])

    # BELOW IS THE BUG
    laddertree = dendropy.Tree()
    laddertree.seed_node = ch1
    print "ladder tree:"
    print(laddertree.as_ascii_plot())
    print (laddertree.as_string(schema='newick'))
    print "ladder leaves:",laddertree.update_taxon_namespace()
    print laddertree.as_ascii_plot()


    print "after reroot:"
    print "subroot:", subroot
    #print "root at: ",laddertree.seed_node.leaf_nodes()[0]
    laddertree.is_rooted = True

    laddertree.reroot_at_node(subroot, update_bipartitions=True, suppress_unifurcations=False)
    print(laddertree.as_ascii_plot())
    print (laddertree.as_string(schema='newick'))
    #ABOVE IS THE BUG

    # print "after reroot:"
    # laddertree_newick = laddertree.as_string(schema='newick')
    # unitree = dendropy.Tree.get(data=laddertree_newick, schema="newick")
    #
    # print "subroot:",subroot
    # print "root at: ",unitree.seed_node.leaf_nodes()[0]
    # unitree.reroot_at_node(unitree.seed_node.leaf_nodes()[0], update_bipartitions=True, suppress_unifurcations=False)
    # print "unitree;"
    # print(unitree.as_ascii_plot())
    # print (unitree.as_string(schema='newick'))

    return laddertree


def create_matrix(nodeList):
    numOfNode = len(nodeList)
    smallMatrix = np.empty([numOfNode, numOfNode])
    for i in range(0, numOfNode):
        if i ==0:
            leaf_i = tree.seed_node
        else:
            leaf_i = nodeList[i].leaf_nodes()[0]
        for j in range(0, numOfNode):
            if j == 0:
                leaf_j= tree.seed_node
            else:
                leaf_j = nodeList[j].leaf_nodes()[0]
            smallMatrix[i][j] = Matrix[dict[leaf_i]][dict[leaf_j]]

    print smallMatrix
    return smallMatrix


argv = sys.argv[1:]
inputmatrixfile = ''
inputpolytomyfile = ''
outputfile = ''
try:
    opts, args = getopt.getopt(argv, "h:m:p:o:", ["m=", "p=", "ofile="])
except getopt.GetoptError:
    print 'test.py -m <distancematrix_file> -p <polytomy_file> -o <outputfile>'
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print 'test.py -m <distancematrix_file> -i <polytomy_file> -o <outputfile>'
        sys.exit()
    elif opt in ("-m"):
        inputmatrixfile = arg
    elif opt in ("-p"):
        inputpolytomyfile = arg
    elif opt in ("-o", "--ofile"):
        outputfile = arg
print 'Input distancematrix_file is ', inputmatrixfile
print 'Input polytomy_file is ', inputpolytomyfile
print 'Output file is ', outputfile

inputmatrix = open(inputmatrixfile, "r")
inputpolytomy = open(inputpolytomyfile, "r")
output = open(outputfile, "w")

lines = inputmatrix.readlines()

# number of taxa
totalTaxa = int(lines[0])

taxaName = []
Matrix = np.zeros((totalTaxa, totalTaxa))

# input distance matrix from resolved tree
for lineNumber in range(1, totalTaxa + 1):
    line = lines[lineNumber].split()
    taxaName.append(line[0][0:])
    for wordNumber in range(1, totalTaxa + 1):
        Matrix[lineNumber - 1][wordNumber - 1] = float(line[wordNumber])
        wordNumber = +1
    lineNumber = +1

# build the polytomy tree
tree_str = inputpolytomy.readlines()[0]

# tree_str ="(182:0.04897350944992166777,(362:0.0627141,380:0.0595683,(688:0.02064480986851693553,654:0.0206829,1036:0.0242252,1035:0.0382441)84:0.00804960075232164472)94:0.02071869672616076519)99:0.03883119450668991862;"
tree = dendropy.Tree.get(data=tree_str, schema="newick")
print "Original:"
print(tree.as_ascii_plot())
leafList = tree.leaf_nodes()

# create a node to matrix dictionary
dict = dict()  # taxadictionary
for i in range(0, totalTaxa):
    for node in leafList:
        if (taxaName[i] == node.taxon.label):
            dict[node] = i

root=tree.seed_node.leaf_nodes()[0]
print tree.seed_node.leaf_nodes()[0]
tree.reroot_at_node(tree.seed_node.leaf_nodes()[0],update_bipartitions=True,suppress_unifurcations=False)
print "After root at leaf at ", tree.seed_node
print(tree.as_ascii_plot())
print (tree.as_string(schema='newick')[5:])
nbj(tree.seed_node)




print "After:"

print(tree.as_ascii_plot())
print (tree.as_string(schema='newick')[5:])
print tree.seed_node.edge_length

print "After root at leaf at ",tree.seed_node.leaf_nodes()[0]
tree.reroot_at_node(tree.seed_node.leaf_nodes()[0],update_bipartitions=True,suppress_unifurcations=False)
print(tree.as_ascii_plot())
print (tree.as_string(schema='newick')[5:])





output.write((tree.as_string(schema='newick'))[5:])


inputpolytomy.close()
inputmatrix.close()
output.close()







