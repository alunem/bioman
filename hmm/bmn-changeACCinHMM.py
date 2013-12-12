#!/usr/bin/env python
# open a HMM file, replace the line "ACC    something" with "ACC       HMMmod_iterator"
# in all files given a path
import string
import re
import argparse
import glob
import sys

parser = argparse.ArgumentParser(description="replace or add (insertion option) the line 'ACC    something' with 'ACC       prefix_iterator in all files given a path'")
parser.add_argument("path", help="the path where the hmm to modify are")
parser.add_argument("-p", "--prefix", default="hmm_", help="the prefix given to the new ACC, default is 'hmm_'")
parser.add_argument("-i", "--insert", default="no", help="if 'yes', insert a ACC line in line 4 instead of replacement")
args = parser.parse_args()


path = args.path
prefix = args.prefix
inspos = args.insert

counter=0
allHMM = glob.glob(path+"/*")
tot = len(allHMM)
mark = range(0, tot, tot/20) 
p = 0

sys.stdout.write("Processing " + str(tot) + " files")
print

### Insert mode
if inspos=="yes":
	for hmm in allHMM:
		if counter in mark: # progress bar
			sys.stdout.write('\r')
			sys.stdout.write("[%-20s] %d%%" % ('='*p, 5*p))
			sys.stdout.flush()
			p+=1
		counter=counter+1
		ins='ACC   '+prefix+str(counter)+'\n'
		with open(hmm, "r") as fhmm:
			lines = fhmm.readlines()
			lines.insert(3,ins)
		with open(hmm, "w") as fhmm:
			for line in lines:
				fhmm.write(line)
### Replace mode
else:
	for hmm in allHMM:
		if counter in mark: # progress bar
			sys.stdout.write('\r')
			sys.stdout.write("[%-20s] %d%%" % ('='*p, 5*p))
			sys.stdout.flush()
			p+=1
		counter=counter+1
		rpl='ACC   '+prefix+str(counter)
		with open(hmm, "r") as fhmm:
			lines = fhmm.readlines()
		with open(hmm, "w") as fhmm:
			for line in lines:
				fhmm.write(re.sub(r'ACC.*', rpl, line))

print
print str(counter), "files processed"
