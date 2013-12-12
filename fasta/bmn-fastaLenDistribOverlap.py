#!/usr/bin/env python
### 


import string
import copy
import sys
from Bio import SeqIO
from StringIO import StringIO
import random

fastafile1 = sys.argv[1]
fastafile2 = sys.argv[2]
seqs1=[]
seqs2=[]
sizes1=[]

handle1 = open(fastafile1)
for seq_record in SeqIO.parse(handle1, "fasta"):
	sizes1.append(len(seq_record.seq))
	seqs1.append(seq_record)

handle1.close()

handle2 = open(fastafile2)
sizes2 = [len(seq_record.seq) for seq_record in SeqIO.parse(handle2, "fasta")]

handle2.close()


def uniq(seq):
	keys = {}
	for e in seq:
		keys[e] = 1
	return keys.keys()

allSizes=uniq(sizes1+sizes2)



distrib1={}
for i in allSizes:
    distrib1[i]=0

distrib2=copy.deepcopy(distrib1)
distribCounter1=copy.deepcopy(distrib1)
distribCounter2=copy.deepcopy(distrib1)

for i in sizes1:
	distrib1[i]+=1

for j in sizes2:
	distrib2[j]+=1

distribCommon={}
for i in allSizes:
	if min(distrib1[i],distrib2[i])!=0:
		distribCommon[i]=min(distrib1[i],distrib2[i])

random.shuffle(seqs1)

handleout1 = open(fastafile1+".overlap", "w")

for i in seqs1:
	seqsize=len(i.seq)
	if distribCommon.has_key(seqsize):
		if distribCounter1[seqsize] < distribCommon[seqsize]:
			SeqIO.write(i, handleout1, "fasta")
			distribCounter1[seqsize]+=1

handleout1.close()

handle2r = open(fastafile2)
for seq_record in SeqIO.parse(handle2r, "fasta"):
	seqs2.append(seq_record)
handle2r.close()

random.shuffle(seqs2)

handleout2 = open(fastafile2+".overlap", "w")

for i in seqs2:
	seqsize=len(i.seq)
	if distribCommon.has_key(seqsize):
		if distribCounter2[seqsize] < distribCommon[seqsize]:
			SeqIO.write(i, handleout2, "fasta")
			distribCounter2[seqsize]+=1

handleout2.close()







