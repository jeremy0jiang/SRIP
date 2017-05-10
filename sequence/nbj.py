#!/usr/bin/python

import sys, getopt
import numpy as np

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
            print 'Input file is "', inputfile
            print 'Output file is "', outputfile

    input = open(inputfile,"r")
    output = open(outputfile,"w")

    lines = input.readlines()

    numOfTaxa= int(lines[0])

    taxa= []
    Matrix = np.zeros((numOfTaxa,numOfTaxa))



    #input matrix
    for lineNumber in range(1,numOfTaxa+1):
        
        line = lines[lineNumber].split()
        taxa.append(line[0])
        for wordNumber in range(1,numOfTaxa+1):
            Matrix[lineNumber-1][wordNumber-1] = float(line[wordNumber])
            wordNumber=+1
        lineNumber=+1

    #create Qmatrix
    QMatrix = np.empty((numOfTaxa,numOfTaxa))
    QMatrix[:] = float("inf")

    for rowNumber in range(0,numOfTaxa):
        for columnNumber in range(rowNumber+1,numOfTaxa):
            QMatrix[rowNumber][columnNumber] = (numOfTaxa-2)*Matrix[rowNumber][columnNumber]-Matrix[rowNumber,:].sum()-Matrix[:,columnNumber].sum()

    min = np.unravel_index(QMatrix.argmin(), QMatrix.shape)

    minRow = min[0]
    minColumn=min[1]

    dist_au= 0.5*Matrix[minRow][minColumn]+float(1)/2/(numOfTaxa-2)*(Matrix[minRow,:].sum()-Matrix[:,minColumn].sum())
    dist_bu= 0.5*Matrix[minRow][minColumn]-float(1)/2/(numOfTaxa-2)*(Matrix[minRow,:].sum()-Matrix[:,minColumn].sum())

    print(1/2/(numOfTaxa-2))
    print(0.5*Matrix[minRow][minColumn])
    print(Matrix[:,minColumn].sum())
    print(dist_bu)
    print(dist_au)
    print(Matrix[minRow][minColumn])

    input.close()
    output.close()





