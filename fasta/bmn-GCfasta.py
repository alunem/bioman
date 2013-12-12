#!/usr/bin/env python
### Draws an histogramm of GC content
### from a fasta file (arg1) , and giving
### a number of histo bins (arg2)
### a name for the graph (arg3)

import string
import sys
from Bio import SeqIO
from StringIO import StringIO
from Bio.SeqUtils import GC
fastafile = sys.argv[1]
nbBins=int(sys.argv[2])

handle = open(fastafile)
gc_values = [GC(seq_record.seq) for seq_record in SeqIO.parse(handle, "fasta")]
gc_values.sort()
handle.close()

import pylab
dataHist=pylab.hist(gc_values,bins=nbBins,range=[0,100])
print fastafile,",",
for i in dataHist[0]:
	print i,",",
print
pylab.title("%i GC ratio \nGC%% %0.1f to %0.1f" \
	% (len(gc_values),min(gc_values),max(gc_values)))
pylab.xlabel("GC%")
pylab.ylabel("Reads")
pylab.show()

