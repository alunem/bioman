#!/usr/bin/env python
### 

import string
import sys
from Bio import SeqIO
from StringIO import StringIO



fastafile = sys.argv[1]
Nseqs = int(sys.argv[2])

print Nseqs

handler = open(fastafile)

record_iterator = SeqIO.parse(handler, "fasta")
while n<Nseqs:
	record = record_iterator.next()
	print format(record, "fasta")
	n+=1

handler.close()




