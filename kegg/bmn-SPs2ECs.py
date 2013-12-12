#!/usr/bin/env python
### à utiliser avec python3.1 !
#	idem blasthits2ECs mais pour les fichiers SPs

import string
import copy
import sys
from collections import Counter

SPfile = sys.argv[1]
SPs2ECs = sys.argv[2]


mapECs={}    # dictionnaire SP -> EC number correspondant


# on ouvre le fichier de mapping pour créer le dictionnaire
f1 = open(SPs2ECs)
for line in f1:
	d = line.find("#")
	mapECs[line[0:d]]=line[(d+1):].strip("\n")

f1.close()


# on compte le nombre de hits pour chaque EC number
rep = 0
EClist = []
dejavu = {}
f2 = open(SPfile)
for line in f2:
	bl1 = line.find(" ")
	motif = line[6:bl1]
	EC = mapECs[motif]
	end_line = line[bl1+1:]
	bl2 = end_line.find(" ")
	seq_id = end_line[7:bl2]
	if seq_id not in dejavu:
		dejavu[seq_id]=set()
		dejavu[seq_id].add(EC)
		EClist.append(EC)
	elif (EC not in dejavu[seq_id]):
		dejavu[seq_id].add(EC)
		EClist.append(mapECs[motif])
		print("bingo!")
	else:
		rep += 1

f2.close()


# on compte le nombre d'occurrences de chaque EC number
cnt = Counter()
for EC in EClist:
	cnt[EC] += 1


# on écrit un fichier avec les décomptes par EC number
outfile = open(SPfile+".ECcounts", "w")
for i in cnt.keys():
	outfile.write(str(i)+" "+str(cnt[i])+"\n")

outfile.write("repetitions %i" % rep)
outfile.close()

