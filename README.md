# SRIP
Usage:
1.	Use newick utility to remove branches
nw_ed 01.inferred.raxml.support.tre 'i & b < 50' o > 01.inferred.raxml.polytomy.tre
2.	Create distance matrix from inferred tree
python computematrix.py -i 01.inferred.raxml.support.tre -o 01.inferred.raxml.support.matrix
3.	Output 
python nbj_one_node.py -m 01.inferred.raxml.support.matrix -p 01.inferred.raxml.polytomy.tre -o 01.inferred.raxml.nbj.tre

Shortcut:

python nbj_one_node.py -m matrix.test -p polytomy.test -o 01.inferred.raxml.nbj.tre
matrix.test is equivalent to 01.inferred.raxml.polytomy.tre
polytomy.test is equivalent 01.inferred.raxml.support.matrix

