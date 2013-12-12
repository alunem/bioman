#!/usr/bin/env python
# the lines should be grouped by queries (as usual, do sort file.blast if not)

import string
import sys
import re


blastres = sys.argv[1]

try:
	Hits=open(blastres, 'r')
except IOError, e:
	print "file not found or unreadable: ",blastres
	pass
	
bestHit=Hits.readline()
maxscore=bestHit.split()[11]
query=bestHit.split()[0]
hits = Hits.readlines()

for hit in hits:
	hitSplit=hit.split()
	if query!=hitSplit[0]:
		print bestHit,
		query=hitSplit[0]
		maxscore=0
		bestHit=hit
	elif maxscore<hitSplit[11]:
		bestHit=hit
		maxscore=hitSplit[11]

Hits.close()

