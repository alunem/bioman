#!/usr/bin/env python
import fileinput
import os
import re
import shutil
import argparse
from argparse import RawTextHelpFormatter
import hashlib

parser = argparse.ArgumentParser(description="""
Copy only uniq HMM models (according to the model itself or optionnaly the CKSUM line)
from a source folder (where models are split, i.e. 1 file => 1 model) to a
destination folder
""", formatter_class=RawTextHelpFormatter)
parser.add_argument("source", help="the folder of split HMMs")
parser.add_argument("destination", help="folder to copy 'dereplicated' HMM")
parser.add_argument("-m", "--model", default=True, help="Model mode (default=True) or checksum mode (if toggled to '0' or 'no') ?")
args = parser.parse_args()

splitHMMpath = args.source
out = args.destination
mode = args.model

if mode != True:
        mode = mode.lower()

T = set(['true','t','1','yes','y',True])
F = set(['false','f','0','no','n'])

if mode in T:
        mode = True
elif mode in F:
        norm = False
else: raise NameError("This is not clear whether you want to use the 'model' or the 'checksum' mode")


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
	if mode==True:
		modelfilter(compFiles)
		print "Running in 'model' mode"
	else:
		print "Running in 'checksum' mode"
		CHKSUMfilter(compFiles)

### Model mode
def modelfilter(files):
	fileinput.close()
	WMID = set() #means Whole model ID set
	allFiles = fileinput.input(files)
	for line in allFiles:
		if line[0:4]=="HMM ": # space is important, because we don't want to catch lines starting with "HMMER3/b [3.0 | March 2010]"
			model = line
			while line[0:2]!="//":
				model = model + line
				line=allFiles.next()
			m = hashlib.md5()
			m.update(model)
			mh = m.hexdigest()
			if mh not in WMID:
				shutil.copy(fileinput.filename(),out)
				WMID.add(mh)

	fileinput.close()


### CHKSUM mode
def CHKSUMfilter(files):
	CKSMlist = set()
	CHK = re.compile('^CKSUM')
	for hmmline in fileinput.input(files):
		result = CHK.search(hmmline)
		if result:
			if hmmline not in CKSMlist:
				shutil.copy(fileinput.filename(),out)
				CKSMlist.add(hmmline)
			fileinput.nextfile()

	fileinput.close()

### call main function
if __name__ == '__main__':
        main()



