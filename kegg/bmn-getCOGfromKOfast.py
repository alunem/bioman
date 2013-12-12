#!/usr/bin/env python

import string
import sys
import re
import marshal

#KOid = "ko:"+str(sys.argv[1])  #example: ko:K00010

ListOfIds = sys.argv[1]

KEGGko_pyc = "/home/manu/scripts/KO.name.desc.COGS.pyc"

try:
	KOs=open(KEGGko_pyc, 'rb')
except IOError, e:
	print "File not found: ",KEGGko_pyc
	pass
	
allKOs=marshal.load(KOs)
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

	
