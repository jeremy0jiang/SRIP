# SRIP
Write a quick summary about what your tool does here.

## Usage
1.	Use [Newick Utilities](http://cegg.unige.ch/newick_utils) to remove low-support branches
    Example: `nw_ed 01.inferred.raxml.support.tre 'i & b < 50' o > 01.inferred.raxml.polytomy.tre`
2.	Create a distance matrix from the inferred tree
    Example: `python computematrix.py -i 01.inferred.raxml.support.tre -o 01.inferred.raxml.support.matrix`
3.	Output
    Example: `python nbj_one_node.py -m 01.inferred.raxml.support.matrix -p 01.inferred.raxml.polytomy.tre -o 01.inferred.raxml.nbj.tre`

## Shortcut

```bash
python nbj_one_node.py -m matrix.test -p polytomy.test -o 01.inferred.raxml.nbj.tre
matrix.test is equivalent to 01.inferred.raxml.polytomy.tre
polytomy.test is equivalent 01.inferred.raxml.support.matrix
```
