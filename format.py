#!/usr/bin/python

import sys, getopt

if __name__ == "__main__":
    argv=sys.argv[1:]
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print('test.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
#            print('Input file is "', inputfile)
#            print('Output file is "', outputfile)

    input = open(inputfile,"r")
    output = open(outputfile,"w")

    count = 0;

    lines = input.readlines()

    output.write('                                   '+'\n')
    for line in lines:
        if count%2==0:
            output.write(line.rstrip('\n')+ " ")
        if count%2==1:
            output.write(line)
            sequence_length=(len(line) - line.count(' ')-line.count('\n'))
        if line.isspace() == False:
            count+=1

    input.close()
    output.close()

    output = open(outputfile,"r+")
    output.write(str(count/2)+' '+str(sequence_length))
    output.close()

