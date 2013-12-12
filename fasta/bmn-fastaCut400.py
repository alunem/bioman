#!/usr/bin/env python
### Script pour Joseph
#	prend en entree un fichier fasta
#	renvoit un fichier fasta contenant les sequences coupees en fragment de 400nt, decalees toutes les 100 nucleotides et
#	de maniere circulaire (a la fin complete les fragments jusqu'a 400nt avec le debut de la sequence)

import string
import copy
import sys

fastafile = sys.argv[1]

f_in = open(fastafile)
f_out = open(fastafile+".cut400", "w")

seq_id = f_in.next().strip("\n")
while (seq_id[0]!=">"):
	seq_id = f_in.next().strip("\n")
while True:
	try:
		seq = f_in.next().strip("\n")
		line = f_in.next().strip("\n")
		while (line[0]!=">"):
			seq = seq+line
			line = f_in.next().strip("\n")
		# ici: seq_id = id et seq = sequence correspondante
		seq_circle = seq+seq[0:400]
		for i in range(0,len(seq),100):
			f_out.write(seq_id+"_%i\n" % i)
			f_out.write(seq_circle[i:(i+400)]+"\n")	
		seq_id = line # pour la prochaine boucle
	except StopIteration:
		break

for i in range(0,len(seq),100):
	f_out.write(seq_id+"_%i\n" % i)
	f_out.write(seq_circle[i:(i+400)]+"\n") # pour prendre en compte aussi la derniere sequenc (break dans le while (line[0]!=">"))

f_in.close()
f_out.close()









