#!/usr/bin/env python
# split a HMM file into several pieces of a chosen amount of HMM models

import sys
import re
import argparse

parser = argparse.ArgumentParser(description="""
splits a HMMer v.3.0 file file into several pieces
of a chosen amount of HMM models
""")
parser.add_argument("hmmfile", help="the HMMer v.3.0 file to break")
group = parser.add_mutually_exclusive_group()
group.add_argument("-n", "--nb_hmm", help="Number of HMM per new file")
group.add_argument("-nf", "--nb_hmmfiles", default=10, help="Number of HMM files")
args = parser.parse_args()


hmmfile = args.hmmfile
nbhmm = args.nb_hmm
nhf = int(args.nb_hmmfiles)

# I don't use the start re but it works
#start=re.compile(r"HMMER3\/b\ \[3\.0\ \|\ March\ 2010\]")

# I use the end instead
end=re.compile(r"//")



if nhf:
    with open(hmmfile, 'r') as modelFile:
        nbh=0
        while True:
            try:
                line = modelFile.next()
                if end.match(line):
                    nbh=nbh+1
            except StopIteration:
                print hmmfile, " contains ", str(nbh), " models"
                nbhmm=nbh/nhf
                break
                

filenb=1
nf=0

with open(hmmfile, 'r') as modelFile:
    nbh=0
    while True:
        try:
            line = modelFile.next()
        except StopIteration:
            print filename, " written"
            print "done"
            subModelFile.close()
            break
        if nbh<=nbhmm:
            if nf!=filenb:
               filename=hmmfile+'.'+str(filenb)
               subModelFile = open(filename, 'w')
               nf=nf+1
               if nf!=1: 
                  subModelFile.write("HMMER3/b [3.0 | March 2010]\n")
            subModelFile.write(line)
            if end.match(line):
                nbh=nbh+1
        else:
            print filename, " written"
            subModelFile.close()
            filenb=filenb+1
            nbh=0

