#!/usr/bin/env python
## working from fasta2ktable.py output to format for esom
import pandas as pd
import numpy as np
import argparse

parser = argparse.ArgumentParser(description="""
Open a kmer tsv (arg 1) (e.g. fasta2ktable output) and format it in a <tab> seperated
esom input file (.lrn). Moreover, it removes columns which contains 0 only. 
'.lrn' format description can be found here: http://databionic-esom.sourceforge.net/user.html#File_formats
""")
parser.add_argument("ktable", help="a ktable file")
parser.add_argument("-s", "--separator", default = "\t", help="the separator to make the output table, default is <tab>")
parser.add_argument("-n", "--name", default = False, help="writes seqnames and kmer names in separeted files")
parser.add_argument("-t", "--transform", default = "sqrt", help="transform kmer frequencies, square-root is the default")
args = parser.parse_args()

ktable = args.ktable
sep = args.separator

kt = pd.DataFrame.from_csv(ktable, sep='\t', header=0)

## removing columns with 0 only
ktsub = kt[kt.columns[(kt != 0).any()]]
if args.transform=='sqrt':
	ktsub = ktsub.apply(np.sqrt)

## writing the .lrn file
n = len(ktsub.index)
m = len(ktsub.columns)+1
s = ["9"]
for i in xrange(m):
    s.append("1")
keys= [i + 1 for i in xrange(n)]
ktsub.insert(0,"key",keys)
out = ktable + '.lrn'
with open (out, 'w') as lrn:
    lrn.write('# lrn esom file generated using "ktable2esom.py '+ ktable + '"\n')
    lrn.write('% '+str(n) + '\n')
    lrn.write('% '+str(m) + '\n')
    lrn.write('% '+ sep.join(s) + '\n')
    lrn.write('% '+ sep.join(ktsub.columns) + '\n')
ktsub.to_csv(out, sep=sep, header=False, index=False, mode='a')


## optional
if args.name:
	## writing rows in file
	with open (ktable+".names", 'w') as frows:
    		frows.write('% '+str(n) + '\n')
		for id,key in zip(ktsub.index, keys):
			frows.write(str(key) + sep + str(id) +'\n')

	## writing columns in file
	with open (ktable+".kmernames", 'w') as fcols:
	    for col in ktsub.columns:
		fcols.write(col+"\n")



