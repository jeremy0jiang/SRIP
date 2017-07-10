#!/usr/bin/python
import dendropy
import sys, getopt
import numpy as np

sys.setrecursionlimit(10000)


def nbj(cur):
    # if (len(tree.leaf_nodes()) != 1000):
    #    print len(tree.leaf_nodes())
    #    sys.exit()
    print "nbj:"
    print "current:", cur

    if cur.is_leaf():
        print "cur is leaf"
        return

    childList = cur.child_nodes()
    print "cur child len", len(cur.child_nodes())
    print "cur child: ", childList
    #print(tree.as_ascii_plot())

    if (len(childList) > 2):

        parent = cur.parent_node
        grandparent = parent.parent_node
        if(grandparent != None ):
            grandparent.remove_child(parent)
            parent_length = parent.edge_length

        print "parent: ",parent



        parent.remove_child(cur)



        combineList=list()
        combineList.append(parent)
        combineList += childList
        subtree = combine(combineList)

        if (grandparent!= None):
            parent.edge_length = parent_length
            grandparent.add_child(parent)
        else:
            print "WRONG!!!!!"
            tree.seed_node = parent

        print "subtree:"
        #print (subtree.as_ascii_plot())
        print "tree here:"
        #print (tree.as_ascii_plot())
        print tree.as_string(schema='newick')

    for child in childList:
        nbj(child)
    return



#For given nodelist, use neighbor joining approach to combine these nodes
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
    #print(laddertree.as_ascii_plot())
    #print (laddertree.as_string(schema='newick'))

    print "ladder leaves:",laddertree.update_taxon_namespace()


    print "laddertree after reroot:"
    print "subroot:", subroot
    #print "root at: ",laddertree.seed_node.leaf_nodes()[0]
    laddertree.is_rooted = True

    laddertree.reroot_at_node(subroot, update_bipartitions=True, suppress_unifurcations=False)
    #print(laddertree.as_ascii_plot())
    #print (laddertree.as_string(schema='newick'))
    #ABOVE IS THE BUG

    return laddertree

#create distance matrix by using different method, such as picking random leaf, two leaves, and closest node
#in this program, I picked a random leaf to calculate distance matrix

def create_matrix(nodeList):
    leftList=nodeList[:]
    rightList = nodeList[:]


    for index in range(0,len(nodeList)):
        cur = nodeList[index]
        if len(cur.child_nodes())==0:
            leftList[index] = cur
        else:
            leftList[index]=cur.leaf_nodes()[0]

    for index in range(0,len(nodeList)):
        cur = nodeList[index]
        if len(cur.child_nodes())==0:
            rightList[index] = cur
        else:
            rightList[index] = cur.leaf_nodes()[1]


    numOfNode = len(nodeList)
    smallMatrix = np.empty([numOfNode, numOfNode])
    i=j=0
    for i in range(0, numOfNode):
        if i == 0:
            print "here"
            i_left = tree.seed_node
            i_right = rightList[(j+1)%numOfNode+1]
            print i_right
        else:
            i_left = leftList[i]
            i_right = rightList[i]
        for j in range(0, numOfNode):
            if j == 0 :
                j_left = tree.seed_node
                j_right = rightList[(j+1)%numOfNode+1]
            else:
                j_left = leftList[j]
                j_right = rightList[j]
            smallMatrix[i][j] = 0.5*(Matrix[dict[i_left]][dict[j_right]]+ Matrix[dict[i_right]][dict[j_left]]- Matrix[dict[i_left]][dict[i_right]]- Matrix[dict[j_left]][dict[j_right]])

    print smallMatrix
    return smallMatrix

if __name__ == '__main__':
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
    num_taxa = int(lines[0])

    taxaName = []
    Matrix = np.zeros((num_taxa, num_taxa))

    # input distance matrix from resolved tree
    for lineNumber in range(1, num_taxa + 1):
        line = lines[lineNumber].split()
        taxaName.append(line[0][0:])
        for wordNumber in range(1, num_taxa + 1):
            Matrix[lineNumber - 1][wordNumber - 1] = float(line[wordNumber])
            wordNumber = +1
        lineNumber = +1

    # build the polytomy tree
    tree_str = inputpolytomy.readlines()[0]

    tree = dendropy.Tree.get(data=tree_str, schema="newick")
    print "Original:"
    #print(tree.as_ascii_plot())
    #print (tree.as_string(schema='newick'))

    leafList = tree.leaf_nodes()


    # create a node name to matrix dictionary
    taxa_dictionary = dict()  # taxadictionary
    for i in range(0, num_taxa):
        for node in leafList:
            if (taxaName[i] == node.taxon.label):
                taxa_dictionary[node] = i


    root=tree.seed_node.leaf_nodes()[0]
    print tree.seed_node.leaf_nodes()[0]
    tree.is_rooted=False

    tree.reroot_at_node(tree.seed_node.leaf_nodes()[0],update_bipartitions=True,suppress_unifurcations=False)
    print "After root at leaf at ", tree.seed_node
    #print(tree.as_ascii_plot())
    #print (tree.as_string(schema='newick'))

    nbj(tree.seed_node)




    print "After:"


    print(tree.as_ascii_plot())
    print (tree.as_string(schema='newick'))
    print tree.seed_node
    tree.seed_node.child_nodes()[0].parent_node = tree.seed_node
    print tree.seed_node.child_nodes()[0].parent_node
    print tree.seed_node.child_nodes()[0].edge_length

    # p= tree.seed_node.child_nodes()[0].child_nodes()[0]
    # print "After reroot at ",p
    # tree.reroot_at_node(p,update_bipartitions=True,suppress_unifurcations=True)
    # print(tree.as_ascii_plot())
    # print (tree.as_string(schema='newick')[5:])





    output.write((tree.as_string(schema='newick'))[5:])


    inputpolytomy.close()
    inputmatrix.close()
    output.close()







