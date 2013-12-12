#!/usr/bin/env python
### ecrit un fichier texte avec la taille de chaque cluster
### exemple : ~/cdhitClusterSizes.py monfichier.clstr

import string
import copy
import sys

clstrfile = sys.argv[1]


f_in = open(clstrfile)
pos = clstrfile.find(".clstr")
f_out = open(clstrfile[0:pos]+"_sizes", "w")

clstr = f_in.next()
while (clstr[0:8]!=">Cluster"):
	clstr = f_in.next()
while True:
	try:
		seq = f_in.next()
		line = f_in.next()
		while (line[0:8]!=">Cluster"):
			if len(line)>1:
				seq = line
			line = f_in.next()
		## ici: clsrt = cluster id et seq = sequence correspondante
		pos = seq.find(" ")
		nb = int(seq[0:pos])+1
		f_out.write(clstr.strip("\n").strip(">")+":%i\n" % nb)
		## fin de ce qu'on fait pour chaque sequence
		clstr = line # pour la prochaine boucle
	except StopIteration:
		break

# pour ne pas oublier la derniere sequence
pos = seq.find(" ")
nb = int(seq[0:pos])+1
f_out.write(clstr.strip("\n").strip(">")+":%i\n" % nb)

f_in.close()
f_out.close()








