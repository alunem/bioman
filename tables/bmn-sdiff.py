#!/usr/bin/env python
# output elements in list 1 than are not in list 2
import sys
import argparse

parser = argparse.ArgumentParser(description="output elements in list 1 <file1> than are not in list 2 <file2>, i.e. elements that are present ONLY in file 1. Each item in the text files are separated with a newline")
parser.add_argument("file1", help="the file that contains list of items to be tested for unique presence, i.e. which are not in file2")
parser.add_argument("file2", help="the file that contains list of items to be suppressed from file 1")
args = parser.parse_args()

f1=args.file1
f2=args.file2

l1=open(f1)
l2=open(f2)

s1=set(l1.readlines())
s2=set(l2.readlines())

l1.close()
l2.close()

s1.difference_update(s2)
for element in s1:
	print element,

#end of program

