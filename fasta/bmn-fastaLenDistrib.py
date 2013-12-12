#!/usr/bin/env python
### Draws an histogramm of sequence lengths
### from a fasta file (arg1) , and giving
### a number of histo bins (arg2)
### a name for the graph (arg3)

import string
import sys
from Bio import SeqIO
from StringIO import StringIO
from Bio.SeqUtils import GC
fastafile = sys.argv[1]
nbBins = int(sys.argv[2])
name = sys.argv[3]

handle = open(fastafile)
sizes = [len(seq_record.seq) for seq_record in SeqIO.parse(handle, "fasta")]
handle.close()

import pylab
pylab.hist(sizes, bins=nbBins)
pylab.title("%s\n%i sequences\nLengths %i to %i" \
	% (str(name), len(sizes),min(sizes),max(sizes)))
pylab.xlabel("Sequence length (bp)")
pylab.ylabel("Count")
pylab.show()

