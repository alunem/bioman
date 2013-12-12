#!/usr/bin/env python
### renvoit une partition du fichier fasta d'origine en deux fichiers fasta
### le premier avec les sequences qui ont un hit >= evalue (blast tableau)
### le deuxieme avec les autres

import string
import copy
import sys
import os
import commands

fastafile = sys.argv[1]
blastfile = sys.argv[2]
evalue = sys.argv[3]

# on recupere les identifiants dont les blast ont une meilleure e-value <= evalue dans un fichier
ids = open(blastfile+".ids", "w")
ids.write(commands.getoutput("awk 'BEGIN{temp='bla'} ($1!=temp){if ($11<=%s) {print $1; temp=$1} else {temp=$1}}' %s" % (evalue,str(blastfile))))
ids.close()

# on creer un ensemble avec tous les identifiants
set_ids = set()
ids = open(blastfile+".ids")
while True:
	try:
		set_ids.add(ids.next().strip("\n"))
	except StopIteration:
		break
ids.close()
os.system("rm %s" % blastfile+".ids")

# on lit le fichier fasta et on ajoute dans l'une ou l'autre des sorties suivant si l'id est dans set_ids ou pas
hit_count=0
nohit_count=0

fasta = open(fastafile)
pos = fastafile.find(".fasta")
fasta_out1 = open(fastafile[0:pos]+"_hits.fasta", "w")
fasta_out2 = open(fastafile[0:pos]+"_mask.fasta", "w")

seq_id = fasta.next()
while (seq_id[0]!=">"):
	seq_id = fasta.next()
while True:
	try:
		seq = fasta.next()
		line = fasta.next()
		while (line[0]!=">"):
			seq = seq+line
			line = fasta.next()
		## ici: seq_id = id et seq = sequence correspondante
		if seq_id.strip(">").strip("\n") in set_ids:
			fasta_out1.write(seq_id+seq)
			hit_count+=1
		else:
			fasta_out2.write(seq_id+seq)
			nohit_count+=1
		## fin de ce qu'on fait pour chaque sequence
		seq_id = line # pour la prochaine boucle
	except StopIteration:
		break

# pour ne pas oublier la derniere sequence
if seq_id.strip(">").strip("\n") in set_ids:
	fasta_out1.write(seq_id+seq)
	hit_count+=1
else:
	fasta_out2.write(seq_id+seq)
	nohit_count+=1

fasta.close()
fasta_out1.close()
fasta_out2.close()


print("Number of hits: %i\nNumber of kept sequences: %i" % (hit_count, nohit_count))





