#!/usr/bin/env python
### 
### example :
### bash$

import string
import sys
proteout = sys.argv[1]

try:
	PO=open(proteout, 'r')
except IOError, e:
	print "Fichier inconnu: ",proteout
	pass
	

lignes = PO.readlines()
fasta=[]
for i in range(len(lignes)):
	if lignes[i][:4]=="prtn":
		print ">" + lignes[i][7:],
		print lignes[i+1][7:],
		

	
