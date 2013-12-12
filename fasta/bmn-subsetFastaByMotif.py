#!/usr/bin/env python
# print sequences only if they contain
# a motif (arg1) in a fasta file (arg2)
import sys
from StringIO import StringIO
from Bio.Seq import Seq
from Bio import SeqIO
from Bio import Motif
from Bio.Alphabet import IUPAC
theMotif = sys.argv[1]
fastafile = sys.argv[2]

momo=Motif.Motif(alphabet=IUPAC.unambiguous_dna)
momo.add_instance(Seq(theMotif,momo.alphabet))

momoc=0
countSeq=0
mySubset=[]

handle = open(fastafile)

def countMotif(myseqrecord, mymotif):
	i=0
	for pos in mymotif.search_instances(myseqrecord.seq):
		i+=1
	return i
			
for seq_record in SeqIO.parse(handle, "fasta"):
	j=countMotif(seq_record,momo)
	if j!=0:
		momoc=momoc + j
		mySubset.append(seq_record)
handle.close()

out_handle = StringIO()
SeqIO.write(mySubset, out_handle, "fasta")
fasta_data = out_handle.getvalue()

print fasta_data
#print "motif",theMotif, "found", momoc, "times in the", fastafile, "file"


