#!/usr/bin/env python
import sys
total = 0

with open(sys.argv[1], 'r') as inp, open('output.txt', 'w') as outp:
   for line in inp:
       try:
           num = float(line)
	   if (num<0):
           	total += num
           outp.write(line)
       except ValueError:
           print('{} is not a number!'.format(line))

print(total)
