#!/usr/bin/env python

import string
import sys
import os
import operator
from collections import Counter


HMMerOUT = sys.argv[1]

#### reading the HMMer OUTPUT file to parse
handle = open(HMMerOUT)
lignes = handle.readlines()
HMMERres=[]

for ligne in lignes:
	if ligne[0]!="#":
		HMMnew = string.split(ligne)
		HMMnew[6] = float(HMMnew[6])
		HMMnew[7] = float(HMMnew[7])
		HMMnew[8] = float(HMMnew[8])
		HMMnew[11] = float(HMMnew[11])
		HMMnew[12] = float(HMMnew[12])
		HMMnew[13] = float(HMMnew[13])
		HMMnew[14] = float(HMMnew[14])
		HMMnew[21] = float(HMMnew[21])
		HMMnew[2] = int(HMMnew[2])
		HMMnew[5] = int(HMMnew[5])
		HMMnew[9] = int(HMMnew[9])
		HMMnew[10] = int(HMMnew[10])
		HMMnew[15] = int(HMMnew[15])
		HMMnew[16] = int(HMMnew[16])
		HMMnew[17] = int(HMMnew[17])
		HMMnew[18] = int(HMMnew[18])
		HMMnew[19] = int(HMMnew[19])
		HMMnew[20] = int(HMMnew[20])
		HMMERres.append(HMMnew[0:22])

##### sort with the key combination (targetName, E-Value)
HMMERres.sort(key = operator.itemgetter(0, 6))
# HMMdex = Counter()
# for word in HMMERres:
# 	HMMdex[word[0]] += 1
# 	print word

for c in HMMERres:
	print c[0], c[5]	


####
# for i,j in HMMERres,HMMdex.keys():
# 	print str(i)+","+str(HMMdex[j])




