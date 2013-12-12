#!/usr/bin/env python
import argparse
import os
import sys
import re

parser = argparse.ArgumentParser(description="Open a fasta file and grep sequences accroding to given expression")
parser.add_argument("expression", help="Expression to look up.")
parser.add_argument("fafile", help="a fasta file")
args = parser.parse_args()

fa=args.fafile
word=args.expression


def main():
	f=fasta2sublist(fa, word)
	printFastaList(f)
		
def parseHeader(rawHeader):
        """ read a header and return id and descr """
        h = rawHeader[1:].strip()
        pos = h.find(" ")
        sID = h[:pos]
        if pos == -1:
                sDEF= ''
        else:
                sDEF= h[h.find(" ")+1:]
        return sID, sDEF


def printFastaList(fasta2list):
	for i in fasta2list:
		print '>' + i[0] + ' ' + i[1] + '\n' + i[2]

def fasta2sublist(fastafile, pattern):
	"""
	reads a fasta file and return a list
	of (ID, description, seq) tuples when
	ID matches pattern. This allows
	header duplicates
	"""
	handle = open(fastafile,'r')
	p = re.compile(pattern)
	seqs = []
	seq_id = handle.next()
	while (seq_id[0]!=">"):
		seq_id = handle.next()
	while True:
		try:
			seq = handle.next().strip()
			line = handle.next()
			while (line[0]!=">"):
				seq = seq+line.strip()
				line = handle.next()
			sid,sdef = parseHeader(seq_id)
			if p.search(sid):
				seqs.append((sid,sdef,seq))
			seq_id = line # last loop
		except StopIteration:
			break
	# last line
	if line[0]!=">":
		seq = seq+line.strip()
	sid,sdef = parseHeader(seq_id)
	if p.search(sid):
		seqs.append((sid,sdef,seq))
	handle.close()
	return seqs


if __name__ == '__main__':
	main()


