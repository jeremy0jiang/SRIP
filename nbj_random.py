#!/usr/bin/python
import dendropy
import sys, getopt
import numpy as np
from sets import Set
from collections import defaultdict
sys.setrecursionlimit(10000)

def nbj(cur):
    if (len(tree.leaf_nodes()) != 1000):
        print len(tree.leaf_nodes())
        sys.exit()
    if (cur.label==True):
        return
    print "nbj:"
    print "current:", cur
    if cur.is_leaf():
        cur.label = True
        print "cur is leaf"
        return


    childList = cur.child_nodes()
    print "cur child len", len(cur.child_nodes())

    print(tree.as_ascii_plot())
    print "cur child: ",childList
    #if (len(childList) > 2 and cur.parent_node != None):
    if((len(childList)>2 and cur != tree.seed_node )or(len(childList)>3 and cur == tree.seed_node ) ):
        tree.reroot_at_node(cur, update_bipartitions=False)
        childList = cur.child_nodes()
        print "to combine these: ", childList
        nd = combine(childList)

        tree.seed_node=nd
        print "after combine"
        print "tree seed",nd
        print(tree.as_ascii_plot())

        for node in nd.child_nodes():
            nbj(node)
        nd.label = True
        return
    elif (len(childList)>0):
        print "childList 1-2: ",childList
        for node in childList:
            nbj(node)
        cur.label=True
        return
    else:
        return



def combine(nodeList):
    numOfNode = len(nodeList)
    smallMatrix = create_matrix(nodeList)

    QMatrix = np.empty([numOfNode, numOfNode])
    QMatrix[:] = float("inf")

    for i in range(0,numOfNode):
        for j in range(i+1,numOfNode):
            QMatrix[i][j]= (numOfNode - 2) * smallMatrix[i][j] - smallMatrix[i,:].sum() - smallMatrix[:,j].sum()


    minRow, minColumn= np.unravel_index(QMatrix.argmin(), QMatrix.shape)
    node_a = nodeList[minRow]
    node_b = nodeList[minColumn]


    dist_au = 0.5 * smallMatrix[minRow][minColumn] + 0.5 / (numOfNode - 2) * (smallMatrix[minRow, :].sum() - smallMatrix[:, minColumn].sum())
    dist_bu = 0.5 * smallMatrix[minRow][minColumn] - 0.5 / (numOfNode - 2) * (smallMatrix[minRow, :].sum() - smallMatrix[:, minColumn].sum())


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
            dist_tocompare[taxa] = (numOfNode- 1) * dist_uk[taxa] - smallMatrix[:, taxa].sum()
        closestTaxa = dist_tocompare.argmin()
        closestNode = nodeList[closestTaxa]

        # distacne from closest node to center
        dist_au = 0.5 * dist_uk[closestTaxa] + 0.5 / (numOfNode - 1) * (smallMatrix[closestTaxa, :].sum() - dist_uk.sum() + dist_uk[closestTaxa])
        dist_uu = 0.5 * dist_uk[closestTaxa] - 0.5 / (numOfNode - 1) * (smallMatrix[closestTaxa, :].sum() - dist_uk.sum() + dist_uk[closestTaxa])

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
        ch1=ch2

    nodeList[0].edge_length = dist_uk[0]
    ch1.add_child(nodeList[0])
    print "combine:"
    print "ch1 child: ", ch1.child_nodes()

    # print(tree.as_string(schema='newick'))
    # print(tree.as_ascii_plot())

    return ch1

def create_matrix(nodeList):
    numOfNode = len(nodeList)
    smallMatrix = np.empty([numOfNode, numOfNode])
    for i in range(0, numOfNode):
        leaf_i = nodeList[i].leaf_nodes()[0]
        for j in range(0, numOfNode):
            leaf_j = nodeList[j].leaf_nodes()[0]
            smallMatrix[i][j] = Matrix[dict[leaf_i]][dict[leaf_j]]

    print smallMatrix
    return smallMatrix



argv = sys.argv[1:]
inputmatrixfile = ''
inputpolytomyfile = ''
outputfile = ''
try:
    opts, args = getopt.getopt(argv, "hm:p:o:", ["m=","p=", "ofile="])
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

#number of taxa
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


#build the polytomy tree
tree_str=inputpolytomy.readlines()[0]

#tree_str ="(182:0.04897350944992166777,(362:0.0627141,380:0.0595683,(688:0.02064480986851693553,654:0.0206829,1036:0.0242252,1035:0.0382441)84:0.00804960075232164472)94:0.02071869672616076519)99:0.03883119450668991862;"
tree = dendropy.Tree.get(data=tree_str,schema="newick")
print "Original:"
print(tree.as_ascii_plot())
leafList = tree.leaf_nodes()

#create a node to matrix dictionary
dict = dict()
for i in range(0,totalTaxa):
    for node in leafList:
        if (taxaName[i]==node.taxon.label):
            dict[node]=i



#tree.reroot_at_node(tree.seed_node, update_bipartitions=False)
nbj(tree.seed_node)



#if(len(cur.child_node_nodes())>=3):
#    nbj(cur.child_node_nodes())



print "After:"
print(tree.as_ascii_plot())
print (tree.as_string(schema='newick'))

output.write((tree.as_string(schema='newick')))

inputpolytomy.close()
inputmatrix.close()
output.close()







