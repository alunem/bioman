#!/usr/bin/env python
# counts reads and nucleotides in fastq a files 

import sys
import argparse

parser = argparse.ArgumentParser(description="counts reads and nucleotides in a fastq file")
parser.add_argument("fastq", help="the fastq file")
args = parser.parse_args()

# from https://code.google.com/p/bioman/source/browse/fastSpeed.py

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

        def is_nuc(self):
                pass

def fastqIterOnce(fastqhandle):
        h = fastqhandle.next()
        s = fastqhandle.next()
        fastqhandle.next()
        q = fastqhandle.next()
        return FastqRecord(h,s,q)
        

nbSeqs=0
nbResidues=0
meanLen=0

with open(args.fastq,"r") as fq:
    while True:
        try:
            r = fastqIterOnce(fq)
            nbSeqs += 1
            nbResidues += r.seqLen()
        except StopIteration:
            meanLen=nbResidues/nbSeqs
            print args.fastq
            print "sequences -- residues -- mean sequence length"
            print nbSeqs,"--",nbResidues,"--", meanLen
            print
            break

