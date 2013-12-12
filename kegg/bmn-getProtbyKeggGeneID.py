#!/usr/bin/env python

from SOAPpy import WSDL
import string
import sys

#geneid example: ko:K00010

ListOfIds = sys.argv[1]

try:
	ids=open(ListOfIds, 'r')
except IOError, e:
	print "Fichier inconnu: ",ListOfIds
	pass
	

wsdl = 'http://soap.genome.jp/KEGG.wsdl'
serv = WSDL.Proxy(wsdl)

lignes = ids.readlines()

for geneid in lignes:
	# retrieve amino acid sequence in a FASTA format
	print serv.bget("-f -n a " + geneid)


	
