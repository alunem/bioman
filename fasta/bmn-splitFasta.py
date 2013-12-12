#!/usr/bin/env python
# split a fasta file in "nbpart" chunks

import string
import sys
import argparse
import os

parser = argparse.ArgumentParser(description="""
split a fasta file in "nbpart" chunks
""")
parser.add_argument("fasta", help="the file that should be split")
parser.add_argument("n", type=int, help="the number of subsets requested")
args = parser.parse_args()

def main():
	splitfasta(args.fasta,args.n,countSeqs(args.fasta))

def countSeqs(fastafile):
    nbseq=0
    with open(fastafile,'r') as fa:
        for line in fa:
            if line[0]==">":
                nbseq+=1
    return nbseq

def splitfasta(fastafile, nbpart, nbtotal):
        """
        split a fasta file in "nbpart" chunks
        The number of seq in in file has to
        be passed (nbtotal)
        """
        modulo=nbtotal%nbpart
        nbSeqsPerFile=nbtotal/nbpart
        if modulo!=0:
            mod=1
            nbSeqsPerFile+=1
        else:
            mod=0
        fa = open(fastafile,'r')
        sid=""
        seq=""
        rec=""
        part=0
    
        for part in xrange(nbpart-mod):
            nbseq=0
            faname=os.path.basename(fastafile) + "." + str(part+1)
            with open(faname,"w") as sfa:
                while nbseq<nbSeqsPerFile:
                    try:
                        line=fa.next()
                        if line[0]==">":
                            rec=sid+seq
                            if rec!="":
                                sfa.write(rec)
                                nbseq+=1
                            sid=line
                            seq=""
                        else:
                            seq+=line
                    except StopIteration:
                        break
                        
              
        #last file if modulo is not 0:
        if mod==1:
            faname=os.path.basename(fastafile) + "." + str(nbpart)
            with open(faname,"w") as sfa:
                sfa.write(sid)
                for line in fa:
                    sfa.write(line)
        else:
            with open(faname,"a") as sfa:
                sfa.write(sid+seq)
                for line in fa:
                    sfa.write(line)
                
        fa.close()

if __name__ == '__main__':
        main()


