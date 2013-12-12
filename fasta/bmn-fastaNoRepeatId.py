#!/usr/bin/env python
### 

import string
import copy
import sys

fastafile = sys.argv[1]

ids={}
f_in = open(fastafile)
f_out = open(fastafile+".norep", "w")

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
		if (not ids.has_key(seq_id)):
			ids[seq_id]=0
			f_out.write(seq_id+seq)
		## fin de ce qu'on fait pour chaque sequence
		seq_id = line # pour la prochaine boucle
	except StopIteration:
		break

if (not ids.has_key(seq_id)):
	ids[seq_id]=0
	f_out.write(seq_id+seq)

f_in.close()
f_out.close()








