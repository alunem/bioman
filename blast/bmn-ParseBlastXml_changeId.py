#!/usr/bin/env python
### prend en entree une e-value et un fichier xml
### renvoit un fichier xml ne contenant que les hits positifs,
### dont la evalue est superieure au seuil et ayant une
### longueur d'alignement superieure a 33 (defaut dans blast2go)

import string
import os
import sys

blastfile = sys.argv[2]  # fichier xml
evalue_cutoff = float(sys.argv[1]) # si on ne veut pas de filtre, il suffit de mettre la evalue utilisee pour le blast ou une plus elevee


# pour rajouter separateur apres un split et changer le hit_id pour que ce soit reconnaissable par blast2go
def add_sep_hit(x):
	begin_hit_def = x.find("<Hit_def>")+9
	end_hit_def = x.find("</Hit_def>")
	hit_def = x[begin_hit_def:end_hit_def]
	begin_hit_id = x.find("<Hit_id>")+8
	end_hit_id= x.find("</Hit_id>")
	hit_id = x[begin_hit_id:end_hit_id]
	# on coupe ce qu'il y a dans hit_def au premier blanc, on met le debut dans hit_id, le reste dans hit_def	
	sp_id,_,_ = hit_def.partition(" ")
	beg,_,end = x.partition(hit_id)
	return "<Hit>"+beg+sp_id+end

def add_sep_hsp(x):
	return "<Hsp>"+x

# doivent etre definies comme globales pour pouvoir les modifier par effets de bords
nb_hits =0
nb_hsps =0

# prend une partie correspondant a un hsp et l'enleve si e-value trop grande
def filter_evalue(x):
	global nb_hsps
	begin_evalue = x.find("<Hsp_evalue>")+12
	end_evalue = x.find("</Hsp_evalue>")
	evalue = float(x[begin_evalue:end_evalue])
	begin_ali_len = x.find("<Hsp_align-len>")+15
	end_ali_len = x.find("</Hsp_align-len>")
	ali_len = int(x[begin_ali_len:end_ali_len])
	if evalue>evalue_cutoff or ali_len<=33:
		beg, sep, end = x.partition("</Hsp>")  # pour garder la fin si c'est le dernier hsp qui est enleve
		nb_hsps -= 1
		return end
	else:
		return x

# filtre les hsps d'un hit et enleve tout le hit s'il n'y a plus de hsps	
def select_hsps(x):
	global nb_hits
	global nb_hsps
	nb_hsps = x.count("<Hsp>")
	hsps = x.split("<Hsp>")
	before_hsps = hsps.pop(0)
	hsps = map(add_sep_hsp, hsps)  # on remet les separateurs
	new_hsps= map(filter_evalue, hsps)
	if nb_hsps<0:
		raise ValueError("negative number of hsps")
	elif nb_hsps==0: # si plus de hsp pour ce hit, on l'enleve
		beg, sep, end = x.partition("</Hit>")  # la fin, a garder si on supprime le dernier hit mais qu'il en reste
		nb_hits -= 1
		return end
	else: 
		return before_hsps+"".join(new_hsps)


## on ouvre les fichiers entree et sortie
f_out = open(blastfile+".hits.%s" % str(evalue_cutoff), "w")
f_in = open(blastfile)


# on ecrit l'entete
header = ""
line = ""
while "<BlastOutput_iterations>" not in line:
	line = f_in.next()
	header += line
f_out.write(header)
line = f_in.next()


# on parse le fichier selon les iterations
# normalement la prochaine ligne que l'on lit est <Iteration>
while "<Iteration>" in line:
	iteration = line
	while "</Iteration>" not in line:
		line = f_in.next()
		iteration += line
	line = f_in.next()
	if "<Hit>" in iteration: # uniquement s'il y a au moins un hit pour cette query
		# on separe en hits
		nb_hits = iteration.count("<Hit>")
		hits = iteration.split("<Hit>")
		before_hits = hits.pop(0)
		hits = map(add_sep_hit, hits)  # on remet les <Hit> qui ont servi a separer iteration
		new_hits= map(select_hsps, hits)
		if nb_hits<0:
			raise ValueError("negative number of hits")
		elif nb_hits>0:
			f_out.write(before_hits+"".join(new_hits))
		# si =0, on ne fait rien, ou oublie cette query


# on ecrit tout ce qu'il reste
while True:
	try:
		f_out.write(line)
		line = f_in.next()
	except StopIteration:
		break
	
f_in.close()
f_out.close()
	













