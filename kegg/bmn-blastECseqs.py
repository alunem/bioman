#!/usr/bin/env python
### Prend en entree un fichier tableau identifiants/EC numbers, un EC number, un fichier fasta et une liste d'identifiants (issus d'un blast)
# 	pour chaque hit du fichier blast, si la sequenque de la base de donnees a pour EC celui en entree, on ecrit la
#	sequence query correspondante dans un nouveau fichier fasta du type nom_fasta_entree.EC_entree
# 	On peut utiliser le script blastDbSeqId.awk sur la sortie de blast pour avoir la liste des identifiants de la base de donnees.
#	Ex: blastECseqs.py uniprotECs 1.7.99.4 bf1.fasta bf1_vs_uniprot.dbid

import string
import copy
import sys

blastfile = sys.argv[4]
ids2ECs = sys.argv[1]
EC = str(sys.argv[2])
fastafile = sys.argv[3]


EC_set = set()   # ensemble des id de la db pour le EC donne

# on ouvre le fichier de mapping pour creer l'ensemble
f1 = open(ids2ECs)
for line in f1:
	id_db = line[0:6]
	EC_file = line[7:].strip("\n")
	if (EC_file == EC):
		EC_set.add(id_db)
		
f1.close()


# on stocke le seq_id que si le db_id est dans l'ensemble
seq_ids = set()
f2 = open(blastfile)
print "sequence de %s pour EC = %s" % (str(fastafile), EC)
for line in f2:
	if (line[0:6] in EC_set):
		seq_ids.add(line[7:].strip("\n"))

f2.close()


# on va chercher les sequences correspondant au seq_ids dans le fichier fasta, et on ecrit dans le nouveau fasta
f3 = open(fastafile)
outfile = open(blastfile+".%s" % EC, "w")

seq_id = f3.next().strip("\n")
while (seq_id[0]!=">"):  # on va à la première ligne du fichier qui commence par un ">"
	seq_id = f3.next().strip("\n")
seq_id = seq_id.strip(">")
while True:
	try:
		seq = f3.next().strip("\n")
		line = f3.next().strip("\n")
		while (line[0]!=">"):
			seq = seq+line
			line = f3.next().strip("\n")
		if (seq_id in seq_ids):
			outfile.write(">"+seq_id+"\n"+seq+"\n")
		seq_id = line.strip(">") 
	except StopIteration:
		break

if (seq_id in seq_ids):
	outfile.write(">"+seq_id+"\n"+seq+"\n")

f3.close()
outfile.close()

