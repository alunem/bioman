#!/usr/bin/env python
### program that subsets a qual file giving a subseted
### fasta file. This works if the sequence ordering is
### preserved between the original fasta, and the 
### (typically with cd-hit-454) subseted one
### example of use: SubsetQual.py F64.454.fasta F64.qual 

import string
import sys
from Bio import SeqIO
from StringIO import StringIO

fastafile = sys.argv[1]
qualfile = sys.argv[2]

outname= fastafile.replace("fasta","qual")
output_handle = open(outname, "w")

fastahandle = open(fastafile)
req=[]
for fasta_record in SeqIO.parse(fastahandle, "fasta"):
	req.append(fasta_record.id)
fastahandle.close()

qualhandle = open(qualfile)
i=0
for seq_record in SeqIO.parse(qualhandle, "qual"):
	if req[i]== seq_record.id:
		i+=1
		SeqIO.write(seq_record, output_handle, "qual")
qualhandle.close()


