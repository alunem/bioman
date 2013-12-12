#!/usr/bin/env python
import sys
import math

prog, fastafile, prefix = sys.argv
print "Sequences are being renamed: >"+prefix+"_1 ...etc"

try:
	input = open(fastafile)
except IOError, e:
	print "File not found: ", fastafile
        pass

outname = "".join(fastafile.split('.')[:-1]) + "."+prefix + ".fasta"
output = open(outname, 'w')

count = 1
# markup = range(0,10**12,10**7)
for line in input.readlines():
	if line.startswith('>'):
		output.write('>%s_%d\n' % (prefix, count))
		count += 1
	else:
		output.write(line)

input.close()
output.close()
print "New fasta file written: ", outname
