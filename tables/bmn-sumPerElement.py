#!/usr/bin/env python
# input file col 1 is an ID
# col2 is a numeric value

import string
import sys


tabfile = sys.argv[1]

try:
	Hits=open(tabfile, 'r')
except IOError, e:
	print "file not found or unreadable: ",tabfile
	pass
	
bestHit=Hits.readline()
query=bestHit.split()[0]
tot=float(bestHit.split()[1])

hits = Hits.readlines()

for hit in hits:
	hitSplit=hit.split()
	if query!=hitSplit[0]:
		print query, str(tot)[:8]
		query=hitSplit[0]
		tot=float(hitSplit[1])
	else:
		tot=float(tot) + float(hitSplit[1])

print query, str(tot)[:8]
Hits.close()

