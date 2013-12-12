#!/usr/bin/env python
import fileinput
import os
import re
import shutil
import argparse
from argparse import RawTextHelpFormatter
import hashlib

parser = argparse.ArgumentParser(description="""
Copy HMM models with a Trusted Cutoff superior to a specified threshold (-t) 
from a source folder (where models are split, i.e. 1 file => 1 model) to a
destination folder
""", formatter_class=RawTextHelpFormatter)
parser.add_argument("source", help="the folder of split HMMs")
parser.add_argument("destination", help="folder to copy 'TC pass' HMM")
parser.add_argument("-t", "--threshold", default=float(1000), help="TC threshold, default = 1000")
args = parser.parse_args()

splitHMMpath = args.source
out = args.destination
TCcut = args.threshold


## verify / create destination folder
if os.path.isdir(out):
	if os.listdir(out):
		raise NameError('Program stopped because given path should be an empty folder')
else: os.mkdir(out)
	

# ls files in source
for root, dirs, files in os.walk(splitHMMpath):
	f1 = files
	r = root

# add their path
compFiles = [r+'/'+f for f in f1]

def main():
	TCfilter(compFiles, TCcut)
	print "Running TC filtering"


### TC filter
def TCfilter(files, cutoff):
	allFiles = fileinput.input(files)
	for line in allFiles:
		if line[0:3]=="TC ":
			TC = line.split()[1]
			if TC=="------":
				fileinput.nextfile()
			else: TC=float(TC)
			if TC<cutoff:
				shutil.copy(fileinput.filename(),out)
			else: fileinput.nextfile()
	fileinput.close()



### call main function
if __name__ == '__main__':
        main()




