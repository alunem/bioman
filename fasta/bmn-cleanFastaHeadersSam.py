#!/usr/bin/env python
### from a fasta file
### cleans up the sequences headers removing spaces and adding a "|"

import string
import sys
fastafile = sys.argv[1]

try:
	ids=open(fastafile, 'r')
except IOError, e:
	print "Fichier inconnu: ",ListOfIds
	pass
	
lignes = ids.readlines()

for ligne in lignes:
	ligne = string.strip(ligne,'\n')
	ligne = string.strip(ligne,'\r')
	if len(ligne)>0:
		if ligne[0]==">":
			b=string.split(ligne,sep="|")
			ligne= ">"+b[1]+"|"+b[2]+ "|" +b[0][1:]+"|"+b[3]
	print(ligne)



