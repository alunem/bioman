#!/usr/bin/env python
### Generates a fastq file from a 454 SFF file

import sys
from Bio import SeqIO
SFFfile = sys.argv[1]

SeqIO.convert(SFFfile, "sff-trim", SFFfile[:-4]+".fastq", "fastq")

