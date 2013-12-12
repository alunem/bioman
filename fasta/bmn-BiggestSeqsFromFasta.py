#!/usr/bin/env python
### Extracts the N longest (default is N=100) sequences from a fasta file 
### needs BioPython

import string
import sys
import argparse
from Bio import SeqIO
from StringIO import StringIO
from operator import itemgetter

parser = argparse.ArgumentParser(description="Extracts the N (default is N=100) sequences from a fasta file ")
parser.add_argument("fastafile", help="the fasta file from which the Nth largest sequences should be extracted")
parser.add_argument("-N", "--number", default=100, type=int, help="the number of sequences to be extracted")
parser.add_argument("-o", "--out", default="output.100.fasta", help="output fasta file")
args = parser.parse_args()


fastafile = args.fastafile
Nseqs = args.number
out= args.out

## should add a precaution
#try:
#   with open(out) as f: 
#except IOError as e:
#   print 'Oh dear.'
#
seqs={}
seqsOrd={}

handle = open(fastafile)
for seq_record in SeqIO.parse(handle, "fasta"):
	seqs[seq_record]=len(seq_record.seq)

handle.close()


seqsOrd = seqs.items()
seqsOrd.sort(key=itemgetter(1),reverse=True)

handle = open(out, "w")
for i in seqsOrd[0:int(Nseqs)]:
	SeqIO.write(i[0], handle, "fasta")
handle.close()

