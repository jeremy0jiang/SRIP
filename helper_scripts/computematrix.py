#!/usr/bin/env python
import dendropy
import numpy as np
import sys, getopt
sys.setrecursionlimit(1000000000)

if __name__ == "__main__":
    argv=sys.argv[1:]
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print 'test.py -i <inputfile> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'test.py -i <inputfile> -o <outputfile>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
#            print 'Input file is "', inputfile
#            print 'Output file is "', outputfile

    input = open(inputfile,"r")
    output = open(outputfile,"w")

    tree = dendropy.Tree.get(path=inputfile,schema="newick")

    pdc = tree.phylogenetic_distance_matrix()
    count=0
    num=0
    numOfNodes = len(tree.taxon_namespace)
    output_string = str(numOfNodes)+"\n"
    
    for i, t1 in enumerate(tree.taxon_namespace[:]):
        output_string += ">" + str(t1.label)+" "
        for t2 in tree.taxon_namespace[:]:
            output_string += str(pdc(t1, t2))+" "
            count += 1
        output_string += "\n"
    output.write(output_string)

input.close()
output.close()


