#!/usr/bin/env python
### ne conserve que les genes appartenant a des contigs dans lesquels se trouvent au moins deux genes

import string
import copy
import sys

fastafile = sys.argv[1]

ids={}
f_in = open(fastafile)
f_out = open(fastafile+".2gcontigs", "w")

tmp = ""
tmp_id = ""
ok = False

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
		## ici: seq_id = id et seq = sequence correspondante
		pos = seq_id.find("NODE")
		if (seq_id[pos:]==tmp_id):
			tmp = tmp+seq_id+seq
			ok = True
		elif ok:
			f_out.write(tmp)
			tmp_id = seq_id[pos:]
			tmp = seq_id+seq
			ok = False
		else:
			tmp_id = seq_id[pos:]
			tmp = seq_id+seq
			ok = False
		## fin de ce qu'on fait pour chaque sequence
		seq_id = line # pour la prochaine boucle
	except StopIteration:
		break

# pour ne pas oublier la derniere sequence
pos = seq_id.find("NODE")
if (seq_id[pos:]==tmp_id):
	f_out.write(tmp+seq_id+seq)
elif ok:
	f_out.write(tmp)

f_in.close()
f_out.close()








