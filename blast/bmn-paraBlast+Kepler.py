#!/usr/bin/env python
### cut a fasta query (arg1) in "nbPart" (arg3)
### subFasta files and launches a blast programm (arg4)
### vs the bank (arg2) for each subfasta and then
### concatenates the tab delimited blast results in
### one file. You can add any additional blastall option in the
### arg5 with quotes like this : "-e 0.001 -a 2 -W 5"
### example of execution :
### paraBlast.py query.fasta blastdb 10 tblastx "-e 0.001 -a 2 -W 5"

### Code modified to be used with new version of blast+
### Modified to be parsed "manually" not using SeqIO, and using a dictionary to store data


import string
import sys
import os
import subprocess
import tempfile
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from StringIO import StringIO

fastafile = sys.argv[1]
#fastafile = "/bank/fasta/Roth/E1.454.fasta"
bank = sys.argv[2]
#bank = "/bank/blastdb/E1"
nbPart=int(sys.argv[3])
#nbPart=int(5)
my_blast_prog = sys.argv[4]
#my_blast_prog = "tblastx"
blastOpt=sys.argv[5]
#blastOpt="-matrix BLOSUM62 -seg yes -evalue 1e-7 -outfmt '6 std frames'"


nbResidues=0
meanLen=0
nbSeqs=0



#### reading the fasta file to cut
handle = open(fastafile)

#seqs=[]
#for seq_record in SeqIO.parse(handle, "fasta"):
#	seqs.append(seq_record)
#	nbSeqs+=1
#	nbResidues+=len(seq_record.seq)

seqs={}
while True:
	try:
		seq_id = handle.next().strip("\n")
		seq = handle.next().strip("\n")
		seqs[seq_id]=seq
		nbSeqs+=1
		nbResidues+=len(seq)
	except StopIteration:
		break

handle.close()



#### prints some infos about the input fasta file
meanLen=nbResidues/nbSeqs

print "sequences -- residues -- mean sequence length"
print nbSeqs,"--",nbResidues,"--", meanLen

#### creates a temp directory and
#### writes the divided-input fasta files into it
wDir= "/scratch/USERS/prestat"
tmpDir=tempfile.mkdtemp(prefix="parablast",dir= wDir)

nbSeqsbyfile=nbSeqs/nbPart
modulo=nbSeqs%nbPart
iteSeqs=0
for i in range(0,nbPart-1):
	tmpFasta=tempfile.mkstemp(dir=tmpDir,suffix="."+str(i)+".fasta")
	#SeqIO.write(seqs[iteSeqs:iteSeqs+nbSeqsbyfile], tmpFasta[1], "fasta")
	out = open(tmpFasta[1], "w")
	for _ in range(nbSeqsbyfile):
		(seq_id, seq)=seqs.popitem()
		out.write(seq_id+"\n"+seq+"\n")
	out.close()
	iteSeqs+=nbSeqsbyfile

tmpFasta=tempfile.mkstemp(dir=tmpDir,suffix="."+str(nbPart)+".fasta")
#SeqIO.write(seqs[iteSeqs:nbSeqs], tmpFasta[1], "fasta")
out = open(tmpFasta[1], "w")
for seq_id in iter(seqs):
	out.write(seq_id+"\n"+seqs[seq_id]+"\n")
out.close()

#### runs the blast
my_blast_files = os.listdir(tmpDir)
myProcesses=[]
for blast_file in my_blast_files:
	cmd= "/grece/prestat/bin/blast+/bin/"+my_blast_prog+" "+\
		"-db"+" "+ bank + " "+\
		"-query"+" "+ tmpDir+"/"+blast_file + " "+\
		"-out"+" "+ tmpDir+"/"+blast_file.replace("fasta","blast") + " "+\
		blastOpt
	myProcesses.append(subprocess.Popen(cmd,shell=True))

#tblastn -db ~/databases/blast/gb_CDS/gb_CDS -query ~/databases/uniprot_reviewed/Ncycle_ECs.fasta -out ~/databases/soap/Ncycle_gb_CDS.blast -evalue 0.0000001 -outfmt '6 std frames' -num_threads 8 

#### waits for the end of all processes
for i in myProcesses:
	i.wait()

#### concatenates the blast files results
#### and removes the temp files used
os.system("cat " + tmpDir+"/"+"*.blast > "+ wDir + '/' + str.split(fastafile,'/')[-1]+".vs."+str.split(bank,'/')[-1]+".blast")
os.system("rm -rf "+ tmpDir)




















