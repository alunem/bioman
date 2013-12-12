#!/usr/bin/env python

import string
import sys
import re

#KOid = "ko:"+str(sys.argv[1])  #example: ko:K00010

ListOfIds = sys.argv[1]
KEGGkoFLAT = sys.argv[2]

try:
	KOs=open(KEGGkoFLAT, 'r')
except IOError, e:
	print "File not found: ",KEGGkoFLAT
	pass
	
allKOs=dict()
cog=""

for koline in KOs.readlines():
	kowords=koline.split()
	if kowords[0]=="ENTRY":
		ko=kowords[1]
	elif kowords[0]=="NAME":
		name=" ".join(kowords[1:])
	elif kowords[0]=="DEFINITION":
		defin=" ".join(kowords[1:])
	elif len(kowords)>2:
		if kowords[1]=="COG:":
			cog=" ".join(kowords[2:])
	elif kowords[0]=="///":
		allKOs[ko]=name+'\t'+defin+'\t'+cog
		cog=""
	else:
		pass

# print allKOs

KOs.close()

try:
        ids=open(ListOfIds, 'r')
except IOError, e:
        print "File not found: ",ListOfIds
        pass

# a gene is something like K22342
KOid = re.compile('K[0-9]{5}')

# open selected functions file

for r in ids:
  result = KOid.search(r)
  if result:
    if result.group(0) in allKOs:
      print r.strip() + '\t' + allKOs[result.group(0)]

ids.close()

	
