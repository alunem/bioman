#!/usr/bin/env python
### reads a fastq file and write a fasta file
### if mean sequence quality is below the (arg 2)
### treshold.
### example 1 : fastq2fasta.py seq.fastq 20
### example 2 : fastq2fasta.py seq.fastq 0 (to keep all reads)

import sys
from Bio import SeqIO
fastqfile = sys.argv[1]
qualcutoff= int(sys.argv[2])
Mean = lambda x: sum(x)/len(x)

good_reads = (rec for rec in \
	SeqIO.parse(fastqfile, "fastq") \
	if Mean(rec.letter_annotations["phred_quality"]) >= qualcutoff)
count = SeqIO.write(good_reads, fastqfile[:-5]+"filt"+str(qualcutoff)+".fasta", "fasta")
print "Saved %i reads" % count


