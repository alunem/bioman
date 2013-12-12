#!/usr/bin/env python
import argparse
import os
import re


parser = argparse.ArgumentParser(description="Filter out seqs which length are out of given limits")
parser.add_argument("fafile", help="a fasta file")
parser.add_argument("-m", "--min", default = 100, help="Minimum sequence length. 0 means there is no limit. Default is 100.")
parser.add_argument("-M", "--max", default = 0, help="Maximum sequence length. Default is 0 which means there is no limit.")
parser.add_argument("-s", "--seqLineLength", default = 60, help="Max elements per sequence line.")
args = parser.parse_args()

fastapath = args.fafile
mini = int(args.min)
maxi = int(args.max)
sll = int(args.seqLineLength)

def main():
	fafile = open(fastapath)
	if maxi==0:
		filterMinAndPrint(fafile,mini)
	elif mini==0:
		filterMaxAndPrint(fafile,maxi)
	elif mini==0 and maxi==0:
		stop("min=0 and max=0: why do you use this program if you don't filter anything?")
	else :
		filterAndPrint(fafile, mini, maxi)
	fafile.close()


def formatseq(seq,linelength):
        """
        Take a seq (without linebreak) and insert line breaks
        after every linelength element
        """
	return '\n'.join(seq[i:i+linelength] for i in xrange(0, len(seq), linelength))

def filterMinAndPrint(fastahandle,minLen):
	"""
	Filters out from a fasta seqs < minLen
	"""
	seq_id = fastahandle.next()
	while (seq_id[0]!=">"):
		seq_id = fastahandle.next()
	while True:
		try:
			seq = fastahandle.next().strip()
			line = fastahandle.next()
			while (line[0]!=">"):
				seq = seq+line.strip()
				line = fastahandle.next()
			if len(seq) >= minLen:
				print seq_id,formatseq(seq,sll)
			seq_id = line # last loop
		except StopIteration:
			break
	# last line
	if (line[0]!=">"):
		seq = seq+line.strip()
	if len(seq) >= minLen:
		print seq_id,formatseq(seq,sll)


def filterMaxAndPrint(fastahandle,maxLen):
	"""
	Filters out from a fasta seqs > maxLen
	"""
	seq_id = fastahandle.next()
	while (seq_id[0]!=">"):  
		seq_id = fastahandle.next()
	while True:
		try:
			seq = fastahandle.next().strip()
			line = fastahandle.next()
			while (line[0]!=">"):  
				seq = seq+line.strip() 
				line = fastahandle.next()
			#print "actual length= ",len(seq)
			if len(seq) <= maxLen:
				print seq_id,formatseq(seq,sll)
			seq_id = line # last loop
		except StopIteration:
			break
	# last line
	if (line[0]!=">"):
		seq = seq+line.strip()
	if len(seq) <= maxLen:
		print seq_id,formatseq(seq,sll)


def filterAndPrint(fastahandle,minLen,maxLen):
	"""
	Filters out from a fasta seqs < minLen
	and seqs > maxLen
	"""
	seq_id = fastahandle.next()
	while (seq_id[0]!=">"):  
		seq_id = fastahandle.next()
	while True:
		try:
			seq = fastahandle.next().strip()
			line = fastahandle.next()
			while (line[0]!=">"):  
				seq = seq+line.strip() 
				line = fastahandle.next()
			#print "actual length= ",len(seq)
			if len(seq) >= minLen and len(seq) <= maxLen:
				print seq_id,formatseq(seq,sll)
			seq_id = line # last loop
		except StopIteration:
			break
	# last line
	if (line[0]!=">"):
		seq = seq+line.strip()
	if len(seq) >= minLen and len(seq) <= maxLen:
		print seq_id,formatseq(seq,sll)


if __name__ == '__main__':
        main()


