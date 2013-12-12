#!/usr/bin/env python
# counts all monomeres in a DNA fasta file
import sys
from Bio.Seq import Seq
from Bio import SeqIO
from Bio import Motif
from Bio.Alphabet import IUPAC
fastafile = sys.argv[1]

A=0
C=0
G=0
T=0
handle = open(fastafile)
for seq_record in SeqIO.parse(handle, "fasta"):
	A=A+seq_record.seq.count("A")
	C=C+seq_record.seq.count("C")
	G=G+seq_record.seq.count("G")
	T=T+seq_record.seq.count("T")
handle.close()
print "A "+ str(A)
print "C "+ str(C)
print "G "+ str(G)
print "T "+ str(T)






