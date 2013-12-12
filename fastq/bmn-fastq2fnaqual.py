#!/usr/bin/env python
import sys
import os
import argparse

parser = argparse.ArgumentParser(description="Extract a fasta and a qual files from a fastq in standard input")
parser.add_argument("fastq", help="A fastq file")
parser.add_argument("-q", "--qual", default="P33", help="Quality encoding: default is 'P33' meaning Phred33 (works for Sanger and Illumina 1.8+, 'solexa' stands for Illumina 1.5+ encoding ")
args = parser.parse_args()
infile = args.fastq
enc = args.qual

#read stdid 
fafile=open(infile)

class FastqRecord:
	"""
	collection of functions intended to process a fastq entry
	as fast as possible
	"""

	def __init__(self, header, sequence, qual):
		self.head = header.strip()
		self.seq = sequence.strip().upper()
		q = r''
		self.qual = (q + qual).strip()

	def __str__(self):
		return self.head + '\n' + self.seq + '\n+\n' + self.qual

	def seqLen(self):
		return len(self.seq)

	def gc(self):
		return round((100 * ((self.seq.count('G') +
					self.seq.count('C'))) /
				len(self.seq)),
				2)

	def toFasta(self):
		return '>' + self.head[1:].strip() + '\n' + self.seq

	def toQual(self, encoding):
		aP33="""!"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJ"""
		aSolexa=""";<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefgh"""
		qdict={}
		q=0
		if encoding=="P33":
			for i in aP33:
				qdict[i]=str(q)
				q+=1
		elif encoding=="solexa":
			for i in aSolexa:
				qdict[i]=str(q)
				q+=1
			qdict["B"]="0"
		qual=[]
		for i in self.qual:
			qual.append(qdict[i])
		return '>' + self.head[1:].strip() + '\n' + ' '.join(qual)

	def is_nuc(self):
		pass

out=os.path.splitext(infile)[0]
fqin=open(infile, 'r')
faout=open(out+'.fasta', 'w')
qualout=open(out+'.qual', 'w')

# First seq
idline=fqin.readline()
seq   =fqin.readline()
spacer=fqin.readline()
quals =fqin.readline()
record=FastqRecord(idline, seq, quals)
faout.write(record.toFasta() + "\n")
qualout.write(record.toQual(enc) + "\n")

while idline:
	idline=fqin.readline()
	seq   =fqin.readline()
	spacer=fqin.readline()
	quals =fqin.readline()
	if idline!="":
		record=FastqRecord(idline, seq, quals)
		faout.write(record.toFasta() + "\n")
		qualout.write(record.toQual(enc) + "\n")

fqin.close()
faout.close()
qualout.close()


