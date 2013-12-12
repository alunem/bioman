#!/usr/bin/env python
### from a file.fasta , removes the leading and
### trailing poly "N" and then delete sequences
### that contain more than (arg 2) percent of "N" 


import sys
from Bio import SeqIO
from Bio.SeqIO.QualityIO import PairedFastaQualIterator
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq

# reads commands
files = sys.argv[1]
Npercent= float(sys.argv[2])

# prepare the output file
outname=files+".pN"+str(int(Npercent))+".fasta"
output_handle = open(outname, "w")


# prepare both (fasta and qual) input files indexing
countN=[]
records = PairedFastaQualIterator(open(files+".fasta"), open(files+".qual"))
for record in records:
	s=list(record)
	for i in range(len(record.letter_annotations['phred_quality'])):
		if record.letter_annotations['phred_quality'][i] < cutoff:
			s[i]="N"
	snew="".join(s).strip("N")
	if snew=="":
		 pass
	else:
		nbN=snew.count("N")
		if (float(nbN)/len(snew))< (Npercent/100):
			countN.append(nbN)
			newrecord = SeqRecord(Seq(snew,), id=record.id, description="length="+str(len(snew)))
			SeqIO.write(newrecord, output_handle, "fasta")
output_handle.close()
print "New fasta written in "+outname
print "This file contains "+ str(sum(countN)/len(countN))+ "N in average within the sequences"

