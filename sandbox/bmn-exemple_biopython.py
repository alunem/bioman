#!/usr/bin/env python
from Bio.Alphabet import IUPAC
bli = Seq("GATCGATGGGCCTATATAGGATCGAAAATCGC", IUPAC.unambiguous_dna) #IUPAC.protein
for index, letter in enumerate(bli):
	print index, letter
	print len(letter)

#nombre de motifs dans la séquence
bli.count("GA")
bli.count("TATA")

#taux de GC:
100 * float(bli.count("G") + bli.count("C")) / len(bli)
#ou sinon:
from Bio.SeqUtils import GC
GC(bli)

#sous-séquence (type Seq), numérotation commence à 0
bli[4:12]
bli[::-1] #retourne la séquences : AGTCC -> CCTGA

#on peut afficher comme on veut en appellant avec %s la séquence
print ">Trilalou\n%s\ncotcot" % bli

bla = Seq("GAGAOULALA", IUPAC.protein)
blu = Seq("TATA", IUPAC.unambiguous_dna)

bli+blu #concatène les séquences
bli+bla #ne fonctionne pas car les alphabets ne sont pas les même (on peut avec generic_alphabet)

banane = Seq("gagaTATA")
banane.upper() #lettres toutes majuscules
banane.lower() #lettres toutes minuscules
#les alphabets IUPAC ne fonctionne qu'en majuscules, si on met lower change en DNAalphabet()

#obtenir le complémentaire ou le renversé du complémentaire (renversé avec [::-1]) que pour nucléotides
bli.complement()
bli.reverse_complement()
bla.complement () #erreur ! les protéines n'ont pas de complément

#on change juste les T en U de la séquence codante pour avoir l'ARNm
arnm = bli.transcribe()
arnm.back_transcribe() #renvoie bli

#traduction. Attention ! Ne marche pas pour les séquences avec gaps.
arnm.translate()
truc = Seq("AGAGAGAGAGTCCTATGATT")
troc = truc.transcribe()
truc.transcribe().translate() #donne : Seq('RERVL*', HasStopCodon(ExtendedIUPACProtein(), '*'))
troc.translate(table="Bacterial") #on peut choisir le code génétique à utiliser (vient du NCBI), ou en plus court table=2, par défaut table=1
troc.translate(to_stop=True) #s'arrête dès qu'il rencontre un codon stop
truc.translate(table=2, stop_symbol="@") #si on veut changer le symbole du codon stop qui est normalement 
truc.translate(cds=True) #il rale : pas de codon start
gene = Seq("GTGAAAAAGATGCAATCTATCGTACTCGCACTTTCCCTGGTTCTGGTCGCTCCCATGGCA" + \
           "GCACAGGCTGCGGAAATTACGTTAGTCCCGTCAGTAAAATTACAGATAGGCGATCGTGAT" + \
           "AATCGTGGCTATTACTGGGATGGAGGTCACTGGCGCGACCACGGCTGGTGGAAACAACAT" + \
           "TATGAATGGCGAGGCAATCGCTGGCACCTACACGGACCGCCGCCACCGCCGCGCCACCAT" + \
           "AAGAAAGCTCCTCATGATCATCACGGCGGTCATGGTCCAGGCAAACATCACCGCTAA")
gene.translate(cds=True) #il rale car GTG normalement pas codon start, mais pour bactéries oui
gene.translate(table="Bacterial", cds=True) #considère la séquence comme une séquence codante complète et applique les conventions en fonction

#manipulation des tables pour la traduction
from Bio.Data import CodonTable
std_table = CodonTable.unambiguous_dna_by_name["Standard"]
bact_table = CodonTable.unambiguous_dna_by_name["Bacterial"]
bact_table.start_codons
bact_table.stop_codons

#pour comparer séquences (attention à l'alphabet)
str(bli) == str(blu) 

#on peut faire des séquences mutables, cf tuto

#pour faire des séquences inconnues, avec des N pour nucléotides et X pour les protéines
from Bio.Seq import UnknownSeq
unk_dna = UnknownSeq(20, alphabet=IUPAC.ambiguous_dna)


#SeqRecord
from Bio.SeqRecord import SeqRecord
help(SeqRecord) #pour voir les différents champs
SeqRecord(bli)
from Bio import SeqIO
machin = SeqIO.read("hao.fasta", "fasta") #pour fichier avec une seule séquence
print machin
print machin.format("fasta")
#mêmes types de choses existent pour les .gnk (format GeneBank)

for seq_record in SeqIO.parse("nosZ.fasta", "fasta"):
    print seq_record.id
    print seq_record.seq
    print len(seq_record)
identifiers = [seq_record.id for seq_record in SeqIO.parse("nosZ.fasta", "fasta")]

nimportequoi = [seq_record.description.split()[1] for seq_record in \  #affiche 2eme ([1]) mot du champ "description"
                SeqIO.parse("nosZ.fasta", "fasta")]
print nimportequoi 


#fonction pour transformer tout un fichier en ses brin complémentaires renversés
def make_rc_record(record):
    """Returns a new SeqRecord with the reverse complement sequence."""
    return SeqRecord(seq = record.seq.reverse_complement(), \
                     id = "rc_" + record.id, \
                     description = "reverse complement")
records = map(make_rc_record, SeqIO.parse("ls_orchid.fasta", "fasta"))
SeqIO.write(records, "rev_comp.fasta", "fasta")
#on peut aussi ajouter une condition
records = (make_rc_record(rec) for rec in SeqIO.parse("ls_orchid.fasta", "fasta") if len(rec)<700)
SeqIO.write(records, "rev_comp_700.fasta", "fasta")




	










