#!/usr/bin/env python
# counts all dinucleotides in a DNA fasta file
import sys
from Bio.Seq import Seq
from Bio import SeqIO
from Bio import Motif
from Bio.Alphabet import IUPAC
fastafile = sys.argv[1]

AA=Motif.Motif(alphabet=IUPAC.unambiguous_dna)
AA.add_instance(Seq("AA",AA.alphabet))
CA=Motif.Motif(alphabet=IUPAC.unambiguous_dna)
CA.add_instance(Seq("CA",CA.alphabet))
GA=Motif.Motif(alphabet=IUPAC.unambiguous_dna)
GA.add_instance(Seq("GA",GA.alphabet))
TA=Motif.Motif(alphabet=IUPAC.unambiguous_dna)
TA.add_instance(Seq("TA",TA.alphabet))
AC=Motif.Motif(alphabet=IUPAC.unambiguous_dna)
AC.add_instance(Seq("AC",AC.alphabet))
CC=Motif.Motif(alphabet=IUPAC.unambiguous_dna)
CC.add_instance(Seq("CC",CC.alphabet))
GC=Motif.Motif(alphabet=IUPAC.unambiguous_dna)
GC.add_instance(Seq("GC",GC.alphabet))
TC=Motif.Motif(alphabet=IUPAC.unambiguous_dna)
TC.add_instance(Seq("TC",TC.alphabet))
AG=Motif.Motif(alphabet=IUPAC.unambiguous_dna)
AG.add_instance(Seq("AG",AG.alphabet))
CG=Motif.Motif(alphabet=IUPAC.unambiguous_dna)
CG.add_instance(Seq("CG",CG.alphabet))
GG=Motif.Motif(alphabet=IUPAC.unambiguous_dna)
GG.add_instance(Seq("GG",GG.alphabet))
TG=Motif.Motif(alphabet=IUPAC.unambiguous_dna)
TG.add_instance(Seq("TG",TG.alphabet))
AT=Motif.Motif(alphabet=IUPAC.unambiguous_dna)
AT.add_instance(Seq("AT",AT.alphabet))
CT=Motif.Motif(alphabet=IUPAC.unambiguous_dna)
CT.add_instance(Seq("CT",CT.alphabet))
GT=Motif.Motif(alphabet=IUPAC.unambiguous_dna)
GT.add_instance(Seq("GT",GT.alphabet))
TT=Motif.Motif(alphabet=IUPAC.unambiguous_dna)
TT.add_instance(Seq("TT",TT.alphabet))
AAc=0
ACc=0
AGc=0
ATc=0
CAc=0
CCc=0
CGc=0
CTc=0
GAc=0
GCc=0
GGc=0
GTc=0
TAc=0
TCc=0
TGc=0
TTc=0


handle = open(fastafile)

def countMotif(myseqrecord, mymotif):
	i=0
	for pos in mymotif.search_instances(myseqrecord.seq):
		i+=1
	return i
			
for seq_record in SeqIO.parse(handle, "fasta"):
	AAc=AAc + countMotif(seq_record,AA)
	ACc=ACc + countMotif(seq_record,AC)
	AGc=AGc + countMotif(seq_record,AG)
	ATc=ATc + countMotif(seq_record,AT)
	CAc=CAc + countMotif(seq_record,CA)
	CCc=CCc + countMotif(seq_record,CC)
	CGc=CGc + countMotif(seq_record,CG)
	CTc=CTc + countMotif(seq_record,CT)
	GAc=GAc + countMotif(seq_record,GA)
	GCc=GCc + countMotif(seq_record,GC)
	GGc=GGc + countMotif(seq_record,GG)
	GTc=GTc + countMotif(seq_record,GT)
	TAc=TAc + countMotif(seq_record,TA)
	TCc=TCc + countMotif(seq_record,TC)
	TGc=TGc + countMotif(seq_record,TG)
	TTc=TTc + countMotif(seq_record,TT)
handle.close()
print
print fastafile
print "AA "+ str(AAc)
print "AC "+ str(ACc)
print "AG "+ str(AGc)
print "AT "+ str(ATc)
print "CA "+ str(CAc)
print "CC "+ str(CCc)
print "CG "+ str(CGc)
print "CT "+ str(CTc)
print "GA "+ str(GAc)
print "GC "+ str(GCc)
print "GG "+ str(GGc)
print "GT "+ str(GTc)
print "TA "+ str(TAc)
print "TC "+ str(TCc)
print "TG "+ str(TGc)
print "TT "+ str(TTc)







