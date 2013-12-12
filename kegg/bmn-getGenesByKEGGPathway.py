#!/usr/bin/env python

from SOAPpy import WSDL
import string
import sys

pathwayID = sys.argv[1]  #example: eco00020

wsdl = 'http://soap.genome.jp/KEGG.wsdl'
serv = WSDL.Proxy(wsdl)

results = serv.get_genes_by_pathway('path:'+pathwayID)
for result in results:
	print result
	
