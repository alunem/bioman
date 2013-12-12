#!/usr/bin/env python
### GeneMark default dna output to fasta
### example :
### bash$ ~/bin/MetaGeneMark_linux64/gmhmmp -d  -m ~/bin/MetaGeneMark_linux64/MetaGeneMark_v1.mod E1.I36.clust1.fasta -o E1.I36.clust1.dna.gff

import string
import sys
GMout = sys.argv[1]

try:
	GM=open(GMout, 'r')
except IOError, e:
	print "Fichier inconnu: ",GMout
	pass
	

lignes = GM.readlines()
fasta=[]
for i in range(len(lignes)):
	if lignes[i][:6]==">gene_":
		while lignes[i]!="\n":
			print lignes[i],
			i+=1


	
