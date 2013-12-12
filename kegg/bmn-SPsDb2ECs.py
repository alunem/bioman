#!/usr/bin/env python
### verif des SPs

import string
import copy
import sys

motiffile = sys.argv[1]
db = sys.argv[2]
motif2ecfile = sys.argv[3]
go2ecfile = sys.argv[4]

motif2dbecs={}
line2ec={}    # dictionnaire numero de ligne -> GOs
motif2ec={} # motif -> EC associe au hit dans SwissProt
go2ec={}      # GO -> EC
motif2ec={}   # motif -> EC



# on creer le dictionnaire GO -> EC
f4 = open(go2ecfile)
for line in f4:
	d = line.find("EC:")
	go2ec[line[0:10]]=line[(d+3):].strip("\n").strip(" ")

f4.close()
print("go2ec construit (fichier go2ec)")

# on creer le dictionnaire numero de ligne (ie sequence) -> EC a l'aide de go2ec
f2 = open(db)
i=0
for line in f2:
	i += 1
	line2ec[str(i)]=set()
	d = line.find("GO:")
	gos = line[d:]
	while (d!=(-1)):
		go = gos[0:10]
		if go in go2ec:
			line2ec[str(i)].add(go2ec[go])
		d = gos.find(" GO:")
		gos = gos[d+1:]

f2.close()
print("line2ec construit (fichier uniprot)")
go2ec.clear()


# on lit le fichier et a chaque ligne on remplit le dictionnaire motif -> ensemble de ECs dans Swissprot
f1 = open(motiffile)
for line in f1:
	motif = line[6:line.find("Seq_id")-1]
	linenum = line[line.find("Seq_id")+7:line.find("Motif_pos")-1]
	ECs = line2ec[linenum]
	if motif in motif2dbecs:
		motif2dbecs[motif].union(ECs)
	else:
		motif2dbecs[motif]=ECs

f1.close()
print("motif2dbecs construit (fichier de motifs)")
line2ec.clear()


# on creer le dictionnaire motif -> EC
f3 = open(motif2ecfile)
for line in f3:
	d = line.find("#")
	motif2ec[line[0:d]]=line[(d+1):].strip("\n").strip("\r")

f3.close()
print("motif2ec construit")

# on ecrit un fichier avec motif:EC * ECs
outfile = open(motiffile+".ECs", "w")
for motif in motif2dbecs:
	outfile.write(motif+":"+motif2ec[motif]+" * ")
	for EC in motif2dbecs[motif]:
		outfile.write(str(EC)+"|")
	outfile.write("\n")

outfile.close()


