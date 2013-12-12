#!/usr/bin/env python
### cut a fasta query (arg1) in "nbPart" (passed by aprun)
### subFasta files and launches a blast+ program (arg3)
### vs the bank (arg2) for each subfasta and then
### concatenates the tab delimited blast results in
### one file. You can add any additional blast+ option in the
### arg4 with quotes like this : "-evalue 0.001 -word_size 5"

import string
import sys
import os
import tempfile
import time
from StringIO import StringIO
from subprocess import call, Popen, PIPE, STDOUT
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
nbPart = comm.Get_size()

def countSeqs(fastafile):
	nbseq=0
	with open(fastafile,'r') as fa:
		for line in fa:
			if line[0]==">":
				nbseq+=1
	return nbseq

def splitfasta(fastafile, nbpart, nbtotal, outdir):
        """
        split a fasta file in "nbpart" chunks
        The number of seq in in file has to
        be passed (nbtotal)
        """
	modulo=nbtotal%nbpart
	nbSeqsPerFile=nbtotal/nbpart
	if modulo!=0:
		mod=1
		nbSeqsPerFile+=1
	else:
		mod=0
	fa = open(fastafile,'r')
	fan = os.path.basename(fastafile)
	sid=""
	seq=""
	rec=""
	part=0

	for part in xrange(nbpart-mod):
		nbseq=0
		faname=outdir+"/"+ fan + "." + str(part+1) + ".fasta"
		with open(faname,"w") as sfa:
			while nbseq<nbSeqsPerFile:
				try:
					line=fa.next()
					if line[0]==">":
						rec=sid+seq
						if rec!="":
							sfa.write(rec)
							nbseq+=1
						sid=line
						seq=""
					else:
						seq+=line
				except StopIteration:
					break

        #last file if modulo is not 0:
	if mod==1:
		faname=outdir+"/"+ fan + "." + str(nbpart) + ".fasta"
		with open(faname,"w") as sfa:
			sfa.write(sid)
			for line in fa:
				sfa.write(line)
	else:
		with open(faname,"a") as sfa:
			sfa.write(sid+seq)
			for line in fa:
				sfa.write(line)

	fa.close()



if comm.rank == 0:
	print "##################################"
	print "Welcome to the Emmanuel Prestat"
	print "MPI wrapper for blast+ "
	print "This run will use " + str(nbPart) + " cores"
	print "job started at "+ time.strftime("%I:%M:%S %p", time.localtime())
	print "##################################"

	##### retrieving user arguments
	fastafile = sys.argv[1]
	fan = os.path.basename(fastafile)
	#fastafile = "/bank/fasta/Roth/E1.454.fasta"
	bank = sys.argv[2]
	#bank = "/bank/blastdb/E1"
	
	my_blast_prog = sys.argv[3]
	#my_blast_prog = "tblastx"
	
	blastOpt=sys.argv[4]
	#blastOpt="-evalue 0.001"

	
	#### prints some infos about the input fasta file
	print "#############################"
	print "query file :", fastafile
	print "that will be blasted vs ", bank
	print "using the program ", my_blast_prog
	print "and the options ", blastOpt
	print "#############################"
	print

	#### creates a temp directory and
	#### writes the divided-input fasta files into it
	cmd = 'echo $SCRATCH'
	p = Popen( cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True )
	scratchdir = p.stdout.read()
	wDir= str.rstrip(scratchdir,"\n")
	tmpDir=tempfile.mkdtemp(prefix="parablast",dir= wDir)
        print "#############################"
        print "tmpDir is: ", tmpDir
        print "#############################"
        print
	splitfasta(fastafile,nbPart,countSeqs(fastafile),tmpDir)	
	
	print "All tmp files are written, it's "+time.strftime("%I:%M:%S %p", time.localtime())
	
	my_blast_files = os.listdir(tmpDir)
	

else:
	my_blast_prog = None
	blastOpt = None
	tmpDir = None
	my_blast_files = None
	bank = None
	
c_my_blast_prog = comm.bcast(my_blast_prog, root=0)
c_blastOpt = comm.bcast(blastOpt, root=0)
c_tmpDir = comm.bcast(tmpDir, root=0)
c_my_blast_files = comm.bcast(my_blast_files, root=0)
c_bank = comm.bcast(bank, root=0)

#Wait until rank 0 is done
comm.barrier()

##### for tests
#print
# print "prog ",c_my_blast_prog , " and my rank is ", rank
# print "opt ",c_blastOpt, " and my rank is ", rank
# print "tmp ",c_tmpDir, " and my rank is ", rank
# print "blast ",c_my_blast_files[rank], " and my rank is ", rank
# print "bank ",c_bank, " and my rank is ", rank


#### runs the blast
cmd2 = c_my_blast_prog+" " + "-db"+" "+ c_bank + " "+ "-query"+" "+ c_tmpDir+"/"+c_my_blast_files[rank] + " "+ "-out"+" "+ c_tmpDir+"/"+c_my_blast_files[rank].replace("fasta","blast") + " "+ "-outfmt '6 std frames' "+	c_blastOpt

##### for tests
# print
# print "My command is \n", cmd2, "\n\nand my rank is ", rank
# print

sts = call( cmd2,shell=True )

#### waits for the end of all processes
comm.Barrier()

#Finish up after all return
if comm.rank == 0:
	#### concatenates the blast files results
	#### and removes the temp files used
	os.system("cat " + tmpDir+"/*.blast > /project/projectdirs/m1317/"+ fan+".vs."+str.split(bank,'/')[-1]+".blast")
	os.system("rm -rf "+ tmpDir)
	print "Please find your blast results in the /project/projectdirs/m1317/"+ fan+".vs."+str.split(bank,'/')[-1]+".blast file"



