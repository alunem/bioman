#!/usr/bin/env python
### from a fasta file
### manip for Sam

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
			c=string.split(string.strip(b[-1],"] "),"[")
			ligne= "> gi|"+str(b[1])+'|'+str(b[0][1:])+'|'+ str(b[2]) +'|'+ str(b[3]) +'|'+ str(b[4])
	print(ligne)



