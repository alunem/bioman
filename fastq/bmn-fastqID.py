#!/usr/bin/env python
import sys
import argparse

parser = argparse.ArgumentParser(description="Subset a fastq file (stdin) by picking reads if header is the same as IDs in file (arg 1)")
parser.add_argument("IDs", help="the file that contains the fastq headers")
args = parser.parse_args()


#get fname from parameter
idfile= args.IDs

#load ids
ids = set( x.strip() for x in open(idfile) )

#read stdid 
handle=sys.stdin 

while ids:
  #parse fastq
  idline=handle.readline()
  seq   =handle.readline()
  spacer=handle.readline()
  quals =handle.readline()
  #check
  id=idline[:-1]
  if id in ids:
    #print fastq
    sys.stdout.write( '%s%s%s%s' % ( idline, seq, spacer, quals ) )
    #update ids
    ids.remove( id )


