#!/usr/bin/env python
import argparse
import screed
import khmer
import os
import sys

parser = argparse.ArgumentParser(description="Open a fasta file (arg 1) and count for each sequence the k-mer frequencies (given a k size in second argument)")
parser.add_argument("fafile", help="a fasta file")
parser.add_argument("ksize", help="the k number. Be aware that the dimension of the output table is n_entries x 4^k.")
parser.add_argument("-s", "--separator", default = "\t", help="the separator to make the output table, default is <tab>")
parser.add_argument("-n", "--normalize", default = False, help="If '-n 1', or '-n True', the values are divided by the total kmers for each entry")
args = parser.parse_args()

fa = args.fafile
sep = args.separator
n = args.normalize
if n != False:
	n = n.lower()

if (n == 'true' or n == 't' or n == '1' or n == 'yes' or n == 'y'):
	norm = True
else:
	norm = False


def main():
	if os.path.isfile(fa + "_screed"):	
		from screed import ScreedDB
		fadb = ScreedDB(fa)
	else:
		fadb = screed.read_fasta_sequences(fa)

	makeKmerArray(fadb,int(args.ksize),norm)

def makeKmerArray(screedb,ksize,normalize):
	"""
	This takes a screedb file and a k-mer size in inputs,
	and print the ktable.
	"""
	ktable = khmer.new_ktable(ksize)
	knames=[]
	print str(ksize) + "-mer" + sep,
	for i in range(0, ktable.n_entries()):
		knames.append(ktable.reverse_hash(i))
	print sep.join(knames)
    	
	if norm:
		for record in screedb.itervalues():
			tot=float()
			kmers=[]
			ktable.clear()
			ktable.consume(str(record.sequence))
			print record.name,
			for i in range(0, ktable.n_entries()):
				kmers.append(ktable.get(i))
				tot=tot+ktable.get(i)
			#print kmers
			kmersNorm = [float(x)/tot for x in kmers]
			#print kmersNorm
			for ele in kmersNorm:
				sys.stdout.write(sep + '%f' % (ele))
			print


	else:
		for record in screedb.itervalues():
			ktable.clear()
			ktable.consume(str(record.sequence))
			sys.stdout.write(record.name)
			for i in range(0, ktable.n_entries()):
			    sys.stdout.write(sep + str(ktable.get(i)))
			print


# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
	main()

