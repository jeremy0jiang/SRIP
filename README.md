# SRIP
Write a quick summary about what your tool does here.

## Usage
Remove low-support branches and use neighbor joining form a ladder-like tree 
1.	Use [Newick Utilities](http://cegg.unige.ch/newick_utils) to remove low-support branches
    Example: `python format.py 01.fas $1 -o  01.format`
             `fastme -i 01.format --dna=F84 -O 01.matrix -g –c`
2.	Create distance matrix from sequence
    Example: `python computematrix.py -i 01.inferred.raxml.support.tre -o 01.inferred.raxml.support.matrix`
3.	Use neighbor joining form a ladder-like tree 
    Example: `python nbj_one_node.py -m 01.inferred.raxml.support.matrix -p 01.inferred.raxml.polytomy.tre -o 01.inferred.raxml.nbj.tre`
## Tools
* **[count_cherries.sh](count_cherries.sh):** Count the number of cherries in a tree
* **[count_polytomies.py](count_polytomies.py):** Count the number of polytomies in a tree
* **[format.py](format.py):** Format the sequence that could be run in fastme



## Shortcut

```bash
python nbj_one_node.py -m matrix.test -p polytomy.test -o 01.inferred.raxml.nbj.tre
matrix.test is equivalent to 01.inferred.raxml.polytomy.tre
polytomy.test is equivalent 01.inferred.raxml.support.matrix
```
