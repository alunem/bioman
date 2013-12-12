#!/usr/bin/env python

from SOAPpy import WSDL
import string
import sys

#KOid = "ko:"+str(sys.argv[1])  #example: ko:K00010

ListOfIds = sys.argv[1]

try:
	ids=open(ListOfIds, 'r')
except IOError, e:
	print "Fichier inconnu: ",ListOfIds
	pass
	

wsdl = 'http://soap.genome.jp/KEGG.wsdl'
serv = WSDL.Proxy(wsdl)

lignes = ids.readlines()

for ligne in lignes:
	KOid = "ko:"+ligne
	results = serv.get_genes_by_ko(KOid, 'all')
	for result in results:
		print str.strip(KOid,"\n")+'\t' +result['entry_id']+'\t'+result['definition']


	
