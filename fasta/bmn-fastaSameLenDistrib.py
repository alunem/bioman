#!/usr/bin/env python
### prend en entree deux fichiers fasta et un seuil (en pourcentage) pour le nombre de N acceptes dans une sequence
# 	renvoit des sous-fichiers de chacun des deux fichiers fasta ayant la meme distribution de taille de sequences
#	elimine au passage les queues poly-N et les sequences contenant plus que le pourcentage seuil de N

# ATTENTION: il ne faut pas qu'il y ait des identifiants identiques -> noRepeatId.py



import string
import copy
import sys

fastafile1 = sys.argv[1]
fastafile2 = sys.argv[2]
seuil = float(sys.argv[3])
seqs1={}    # dictionnaire taille de sequence -> dictionnaire de sequences de cette taille
seqs2={}
distrib={}  # correspond a la difference entre les distributions


## on ouvre premier fichier
f1 = open(fastafile1)

# initialisation, on cherche le premier >
seq_id = f1.next().strip("\n")
while (seq_id[0]!=">"):
	seq_id = f1.next().strip("\n")
seq_id = seq_id.strip(">")
while True:
	try:
		seq = f1.next().strip("\n")
		line = f1.next().strip("\n")
		while (line[0]!=">"):
			seq = seq+line
			line = f1.next().strip("\n")
		# ici : seq_id = id et seq = sequence correspondante
		seq = seq.strip("N") # on enleve queue poly-N
		nbN = seq.count("N")
		l = len(seq)
		pN = float(1.0)
		if (pN < seuil):
			distrib[l]=distrib.get(l,0)+1    # +1 des qu'il y a une sequence de taille l dans 1er fichier
			if (not seqs1.has_key(l)): 
				seqs1[l]={}
			seqs1[l][seq_id]=seq      # seqs[l] = dictionnaire: identifiant -> sequences
		# pour la boucle suivante :
		seq_id = line.strip(">")
	except StopIteration:
		break

# pour faire meme chose sur la derniere sequence (on sort de la boucle avant)
seq = seq.strip("N")
	nbN = seq.count("N")
	l = len(seq)
	pN = float(1.0)
	if (pN < seuil):
		distrib[l]=distrib.get(l,0)+1
		if (not seqs1.has_key(l)): 
			seqs1[l]={}
		seqs1[l][seq_id]=seq

f1.close()



## pour le deuxieme fichier, on ne regarde que la taille pour ne pas tout avoir en memoire en meme temps
f2 = open(fastafile2)

# initialisation, on cherche le premier ">"
seq_id = f2.next().strip("\n")
while (seq_id[0]!=">"):
	seq_id = f2.next().strip("\n")
seq_id = seq_id.strip(">")
while True:
	try:
		seq = f2.next().strip("\n")
		line = f2.next().strip("\n")
		while (line[0]!=">"):
			seq = seq+line
			line = f2.next().strip("\n")
		# ici : seq_id = id et seq = sequence correspondante
		seq = seq.strip("N") # on enleve queue poly-N
		nbN = seq.count("N")
		l = len(seq)
		pN = float(1.0)
		if (pN < seuil):
			distrib[l]=distrib.get(l,0)-1   # -1 des qu'il y a une sequence de taille l dans le 2eme fichier
		# pour la boucle suivante :
		seq_id = line.strip(">")
	except StopIteration:
		break

# pour faire meme chose sur la derniere sequence (on sort de la boucle avant)
seq = seq.strip("N")
	nbN = seq.count("N")
	l = len(seq)
	pN = float(1.0)
	if (pN < seuil):
		distrib[l]=distrib.get(l,0)-1

f2.close()



# si plus dans fichier 1, on enleve autant de sequences qu'il faut (=nombre dans distrib)
for i in iter(distrib):
	n = distrib[i]
	if (n>0): # il y a n  sequences en trop dans le fichier 1
		for _ in range(n):
			_ = seqs1[i].popitem()  # enleve un element du dictionnaire au hasard





# on ecrit dans fichier sortie
f1_out = open(fastafile1+".overlap", "w")
for l in iter(seqs1):
	for i in iter(seqs1[l]):
		f1_out.write(">"+i+"\n"+seqs1[l][i]+"\n")

f1_out.close()
seqs1.clear() # on elimine les sequences en memoire du fichier 1



## on refait tout pareil pour le fichier 2
f2bis = open(fastafile2)

# initialisation, on cherche le premier ">"
seq_id = f2bis.next().strip("\n")
while (seq_id[0]!=">"):
	seq_id = f2bis.next().strip("\n")
seq_id = seq_id.strip(">")
while True:
	try:
		seq = f2bis.next().strip("\n")
		line = f2bis.next().strip("\n")
		while (line[0]!=">"):
			seq = seq+line
			line = f2bis.next().strip("\n")
		# ici : seq_id = id et seq = sequence correspondante
		seq = seq.strip("N") # on enleve queue poly-N
		nbN = seq.count("N")
		l = len(seq)
		pN = float(1.0)
		if (pN < seuil):
			if (not seqs2.has_key(l)): 
				seqs2[l]={}
			seqs2[l][seq_id]=seq
		# pour la boucle suivante :
		seq_id = line.strip(">")
	except StopIteration:
		break

# pour faire meme chose sur la derniere sequence (on sort de la boucle avant)
seq = seq.strip("N")
	nbN = seq.count("N")
	l = len(seq)
	pN = float(1.0)
	if (pN < seuil):
		if (not seqs2.has_key(l)): 
			seqs2[l]={}
		seqs2[l][seq_id]=seq

f2bis.close()



for i in iter(distrib):
	n = distrib[i]
	if (n<0):   # cette fois ci, il y a trop de sequences si n est negatif
		try:
			for _ in range(-n):
				_ = seqs2[i].popitem()
		except KeyError:
				print "seqs2[i] est vide avec (i,n)=(%i,%i)" % i n


f2_out = open(fastafile2+".overlap", "w")
for l in iter(seqs2):
	for i in iter(seqs2[l]):
		f2_out.write(">"+i+"\n"+seqs2[l][i]+"\n")

f2_out.close()










