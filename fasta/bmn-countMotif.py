#!/usr/bin/env python
# counts a motif (arg1) with overlaps in a fasta file (arg2)
import sys
from Bio.Seq import Seq
from Bio import SeqIO
from Bio import Motif
from Bio.Alphabet import IUPAC
theMotif = sys.argv[1]
fastafile = sys.argv[2]

momo=Motif.Motif(alphabet=IUPAC.unambiguous_dna)
momo.add_instance(Seq(theMotif,momo.alphabet))

momoc=0

handle = open(fastafile)

def countMotif(myseqrecord, mymotif):
	i=0
	for pos in mymotif.search_instances(myseqrecord.seq):
		i+=1
	return i
			
for seq_record in SeqIO.parse(handle, "fasta"):
	momoc=momoc + countMotif(seq_record,momo)
handle.close()

print "motif",theMotif, "found", momoc, "times in the", fastafile, "file"


