#!/usr/bin/env python
### a utiliser avec python3.1 ! (pas directement en executable)
### prend en entree un fichier de sortie tableau blast et un fichier avec deux colonnes identifiant/EC 
#	renvoit un fichier texte donnant le nombre de hits par EC number dans le fichier blast
#   Ex: python3.1 blasthits2ECs.py blabla.blast uniprot2ECs


import string
import copy
import sys
from collections import Counter

blasthitfile = sys.argv[1]
ids2ECs = sys.argv[2]


mapECs={}    # dictionnaire id -> EC number correspondant


# on ouvre le fichier de mapping pour créer le dictionnaire
f1 = open(ids2ECs)
for line in f1:
	mapECs[line[0:6]]=line[7:].strip("\n")

f1.close()


# on compte le nombre de hits pour chaque EC number
EClist = []
f2 = open(blasthitfile)
for line in f2:
	EClist.append(mapECs[line.strip("\n")])

f2.close()


# on compte le nombre d'occurrences de chaque EC number
cnt = Counter()
for EC in EClist:
	cnt[EC] += 1


# on écrit un fichier avec les décomptes par EC number
outfile = open(blasthitfile+".ECcounts", "w")
for i in cnt.keys():
	outfile.write(str(i)+" "+str(cnt[i])+"\n")

outfile.close()

