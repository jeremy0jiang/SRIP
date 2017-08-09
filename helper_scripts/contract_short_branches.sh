#!/bin/bash
# USAGE: ./contract_short_branches.sh <input_file> <output_file> <threshold>
/Users/jeremyjiang/Desktop/SRIP/helper_scripts/label_short_branches.py -i $1 -t $3| nw_ed - 'i & b < 50' o > $2
