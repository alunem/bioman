#!/usr/bin/env python
### Prend en entree un fichier fasta et un fichier .clstr de cd-hit correspondant a ce fasta trie par ordre decroissant (clstr_sort_by.pl)
# de taille de clusters, ainsi que le nombre de clusters a plusieurs sequences (on peut l'avoir avec plot_len1.pl)

# fichier fasta doit etre une ligne sur deux, sans ligne vide, etc.

import string
import copy
import sys

fastafile = sys.argv[1]
clstrfile = sys.argv[2]
nbclstr = int(sys.argv[3])

seqs = {}

# on met le fichier fasta en memoire comme un dictionnaire identifiant -> sequence
f1 = open(fastafile)
seq_id = f1.next().strip("\n")
while (seq_id[0]!=">"):
	seq_id = f1.next().strip("\n")
	espace = seq_id.find(" ")
	if (espace!=-1):  # si on trouve un espace
		seq_id = seq_id[0:espace]   # tout l'identifiant fasta avant le premier espace (c'est comme ca que coupe cdhit)
while True:
	try:
		seq = f1.next().strip("\n")
		line = f1.next().strip("\n")
		while (line[0]!=">"):
			seq = seq+line
			line = f1.next().strip("\n")
		seqs[seq_id.strip(">")]=seq
		seq_id = line
		espace = seq_id.find(" ")
		if (espace!=-1): 
			seq_id = seq_id[0:espace] 
	except StopIteration:
		break

seqs[seq_id.strip(">")]=seq  # pour prendre en compte aussi la derniere sequenc (break dans le while (line[0]!=">"))

f1.close()


# on lit le fichier .clstr dans l'ordre et on ecrit sequences correspondantes, on s'arrete au nbclstr-ieme cluster. 
f2 = open(clstrfile)
f_out = open(clstrfile+".seq", "w")
line = f2.next().strip("\n")  # normalement ">Cluster 0"
for i in range(0, nbclstr):
	if (line[0:8]!=">Cluster"):
		print("Ca marche pas ton truc !\n")
		break
	line = f2.next().strip("\n")
	debut = line.find(">")
	fin = line.find("... *")
	seq_id = line[debut+1:fin]
	if seq_id in seqs:
		f_out.write(">"+seq_id+"\n"+seqs[seq_id]+"\n")
	else:
		print("%s pas de le dico seq_id/seq" % seq_id)
	while (line[0:8]!=">Cluster"):
		line = f2.next().strip("\n")

f2.close()
f_out.close()








