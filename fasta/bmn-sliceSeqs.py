#!/usr/bin/env python
# import libraries
import argparse
import screed
import os
import re


parser = argparse.ArgumentParser(description="Slice each sequence from a fasta file into pieces of length l. The last slice might be smaller.")
parser.add_argument("fafile", help="a fasta file")
parser.add_argument("-l", "--seqlength", default = 100, help="The length of the slices to be output.")
args = parser.parse_args()

fa = args.fafile
maxSlice = int(args.seqlength) - 1

def main():
        if os.path.isfile(fa + "_screed"):      
                from screed import ScreedDB
                fadb = ScreedDB(fa)
        else:
                fadb = screed.read_fasta_sequences(fa)

	makeSlices(fadb,maxSlice)

def makeSlices(screedb,outlen):
	splitSlices = re.compile(r".{1,%s}" % outlen , re.DOTALL).findall	
	for record in screedb.itervalues():
		seqname = record.name
		i = 1
		for piece in splitSlices(str(record.sequence)):
			print ">"+seqname + "-" + str(i) + "-" + str(len(piece)+1) + "bp"
			print piece
			i = i + 1

if __name__ == '__main__':
        main()

