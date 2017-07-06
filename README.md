# SRIP
Usage:<br />
1.	Use newick utility to remove branches<br />
nw_ed 01.inferred.raxml.support.tre 'i & b < 50' o > 01.inferred.raxml.polytomy.tre
2.	Create distance matrix from inferred tree<br /><br />
python computematrix.py -i 01.inferred.raxml.support.tre -o 01.inferred.raxml.support.matrix
3.	Output <br />
python nbj_one_node.py -m 01.inferred.raxml.support.matrix -p 01.inferred.raxml.polytomy.tre -o 01.inferred.raxml.nbj.tre

Shortcut:<br />

python nbj_one_node.py -m matrix.test -p polytomy.test -o 01.inferred.raxml.nbj.tre<br />
matrix.test is equivalent to 01.inferred.raxml.polytomy.tre<br />
polytomy.test is equivalent 01.inferred.raxml.support.matrix<br />

