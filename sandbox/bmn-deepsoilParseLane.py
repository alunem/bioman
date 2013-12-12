#!/usr/bin/env python
### Script pour rajouter le nom du fichier dans l'entete fasta : entete type >bf1.blabla (prend en entree le cat de tous les barefallow)
#	utile pour le script de matrice de rammcap (il separe les echantillons en fonction de ce qu'il y a avant le premier . dans l'entete fasta

# Attention pour Barefallow: caractère 10, pour Grassland: caractère 11 (tout remplacer par gl et 10 par 11)

import string
import copy
import sys

fastafile = sys.argv[1]

f_in = open(fastafile)
bf1 = open("bf1.fasta", "w")
bf2 = open("bf2.fasta", "w")
bf3 = open("bf3.fasta", "w")
bf4 = open("bf4.fasta", "w")
bf6 = open("bf6.fasta", "w")
bf7 = open("bf7.fasta", "w")
bf8 = open("bf8.fasta", "w")

seq_id = f_in.next()
while (seq_id[0]!=">"):
	seq_id = f_in.next()
while True:
	try:
		seq = f_in.next()
		line = f_in.next()
		while (line[0]!=">"):
			seq = seq+line
			line = f_in.next()
		# ici: seq_id = id et seq = sequence correspondante
		if (seq_id[10]=="1"):
			bf1.write(seq_id+seq)
		elif (seq_id[10]=="2"):
			bf2.write(seq_id+seq)
		elif (seq_id[10]=="3"):
			bf3.write(seq_id+seq)
		elif (seq_id[10]=="4"):
			bf4.write(seq_id+seq)
		elif (seq_id[10]=="6"):
			bf6.write(seq_id+seq)
		elif (seq_id[10]=="7"):
			bf7.write(seq_id+seq)
		elif (seq_id[10]=="8"):
			bf8.write(seq_id+seq)
		else:
			print "mauvaise syntaxe d'identifiant:%s" % seq_id
			break
		seq_id = line # pour la prochaine boucle
	except StopIteration:
		break

if (seq_id[10]=="1"):  # pour prendre en compte la derniere sequence
	bf1.write(seq_id+seq)
elif (seq_id[10]=="2"):
	bf2.write(seq_id+seq)
elif (seq_id[10]=="3"):
	bf3.write(seq_id+seq)
elif (seq_id[10]=="4"):
	bf4.write(seq_id+seq)
elif (seq_id[10]=="6"):
	bf6.write(seq_id+seq)
elif (seq_id[10]=="7"):
	bf7.write(seq_id+seq)
elif (seq_id[10]=="8"):
	bf8.write(seq_id+seq)
else:
	print "mauvaise syntaxe d'identifiant:%s" % seq_id


f_in.close()
bf1.close()
bf2.close()
bf3.close()
bf4.close()
bf6.close()
bf7.close()
bf8.close()









