#!/usr/bin/env python
import string
import re
import argparse
import sys

parser = argparse.ArgumentParser(description="Return a ko 'number -- description' table given a genuine ko flat file")
parser.add_argument("kofile", help="the KEGG ko file")
parser.add_argument("-s", "--separator", default="\t", help="the seprator used to add the complement information, default is <tab>")
args = parser.parse_args()

kofname = args.kofile
sep = args.separator

try:
        kos=open(kofname, 'r')
except IOError, e:
        print "file not found or unreadable: ", kofname
        pass

## print the first line
words = kos.readline().split()
if words[0]=="ENTRY":
	print words[1],

lines=kos.readlines()

## print the rest
for line in lines:
	words = line.split()
	if words[0]=="ENTRY":
		print "\n"+words[1],
	elif words[0]=="DEFINITION":
		print sep+" ".join(words[1:]),

