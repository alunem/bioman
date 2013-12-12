#!/usr/bin/env python
### Counts several elements in a fasta file:
### the nb of sequences, of residues, and the
### mean sequence length


import string
import sys
from Bio import SeqIO
from StringIO import StringIO
fastafile = sys.argv[1]

nbSeqs=0
nbResidues=0
meanLen=0

handle = open(fastafile)
for seq_record in SeqIO.parse(handle, "fasta"):
	nbSeqs+=1
	nbResidues+=len(seq_record.seq)
handle.close()

meanLen=nbResidues/nbSeqs

print fastafile
print "sequences -- residues -- mean sequence length"
print nbSeqs,"--",nbResidues,"--", meanLen
print


