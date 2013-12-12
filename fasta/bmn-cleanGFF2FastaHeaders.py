#!/usr/bin/env python
### from a GFF2fasta.py fasta file output
### cleans the header and adds a sequence numbering


import string
import sys
fastafile = sys.argv[1]

try:
	ids=open(fastafile, 'r')
except IOError, e:
	print "Fichier inconnu: ",fastafile
	pass
	
lignes = ids.readlines()
uniqID=0

for ligne in lignes:
	ligne = string.strip(ligne,'\n')
	ligne = string.strip(ligne,'\r')
	if len(ligne)>0:
		if ligne[0]==">":
			uniqID=uniqID+1
			b=string.split(ligne,sep=">")
			ligne= ">"+str(uniqID)+"-"+str(string.split(b[2]," ")[0])+str(b[1])
	print(ligne)




