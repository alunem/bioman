#!/usr/bin/env python
import string
import sys
import os
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from StringIO import StringIO
import random
import tempfile


fastafile = sys.argv[1]
#fastafile = "/bank/fasta/Roth/E1.454.fasta"
randomYorN = sys.argv[2]
nbPart=int(sys.argv[3])
#nbPart=int(5)

seqs=[]
nbSeqs=0

handle = open(fastafile)
for seq_record in SeqIO.parse(handle, "fasta"):
	seqs.append(seq_record)
	nbSeqs+=1

handle.close()

if randomYorN.lower()=="yes":
	random.shuffle(seqs)
elif randomYorN.lower()!="no":
	print("The second argument should be yes or no. Do you want to randomize the sequences before dividing the fasta file ?")

#### writes the divided-input fasta files into it

nbSeqsbyfile=nbSeqs/nbPart
modulo=nbSeqs%nbPart
iteSeqs=0

for i in range(0,nbPart-1):
	handleout = open("part"+str(i+1)+"."+fastafile, "w")
	SeqIO.write(seqs[iteSeqs:iteSeqs+nbSeqsbyfile], handleout, "fasta")
	iteSeqs+=nbSeqsbyfile

handleout = open("part."+str(nbPart)+"."+fastafile, "w")
SeqIO.write(seqs[iteSeqs:nbSeqs], handleout, "fasta")



