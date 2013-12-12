#!/usr/bin/env python

##### programm that extracts bank seq ids from
##### a blast result default flat file.
##### Typical use : ./HSPextraction.blast file.blast ncbi
##### use 454 instead of ncbi if the blastdb has been formated from
##### a 454 generated fasta file.

import string
import sys
from Bio.Blast import NCBIStandalone 
blastfile = sys.argv[1]
blastdbOrigin = sys.argv[2] # 454 or ncbi

#result_handle = open("/home/alban/NPTIIdansPyro/NPTIIvsNT.blast")
result_handle = open(blastfile)
blast_parser = NCBIStandalone.BlastParser()
blast_record = blast_parser.parse(result_handle)

if (blastdbOrigin=='454'):
	for alignment in blast_record.alignments:
		print str(alignment)[1:15]
else:
	for alignment in blast_record.alignments:
		print string.split(str(alignment), '|')[1]


