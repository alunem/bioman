#!/usr/bin/env python

#################################################################################
# spe2newick transforme l'ecriture 'ligne par ligne' d'un arbre phylogenetique	#
# comme utilise dans postgresql avec le type 'ltree', en format Newick	sur	#
# la sortie standard								#
#										#
# 27 avril 2005                                                                 #
# Emmanuel PRESTAT								#
#################################################################################
print "Content-Type: text/html"
print
import cgi
import cgitb; cgitb.enable()
import sys, string
import time

# ouverture du fichier en lecture dont le nom est en premier argument
#

form=cgi.FieldStorage()
fe=file(form['monfichier'].value,'r')

# lecture du fichier ouvert
#
lines = fe.readlines()
id=string.split(lines[0]).index('species_id')
name=string.split(lines[0]).index('species_name')
access=string.split(lines[0]).index('access_number')
path=string.split(lines[0]).index('tree_position')
longueur=string.split(lines[0]).index('length')
entry=[]
for i in lines:
    line=''
    mots=string.split(i)
    mots[name]=mots[name].replace('(','').replace(')','').replace('[','').replace(']','').replace(',','').replace(':','').replace(' ','')
    line=mots[path]+'\t'+mots[id]+'[&&NHX:S='+mots[name]+':E='+mots[access]+']'
    entry.append(line)
#     Ajout de Coli pour faire un repère
    entry.append("Top.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.2\tEscColi***TAG_SPECIES***[&&NHX:S=Escherichia_coli:E=X80731]")
    



# chaque ligne de donnee est mise dans une liste (1) puis chaque chemin
# devient une liste de noeuds (2), chaque noeud redondant est supprime (3)
#
def brut2elabore(lignes):
	donnees=[]	
	for ligne in lignes:				# etape (1)
		mots=string.split(ligne)
		mots[0]=string.split(mots[0],'.')	# etape (2)
		if mots[0][0]=='Top':
			mots[0]=mots[0][1:]
			mots[0].append('f')		   # signal de fin
			donnees.append(mots)
	donnees.sort()
	v=[]						# etape (3)
	for i in donnees:				   # on regarde quel est le chemin min
		v.append(i[0])
	mini=len(v[0])
	for i in v:
		if mini>len(i):
			mini=len(i)
	w=[]
	for j in range(mini):				   # on regarde dans l'espace du chemin min, quels
		v=[]					   # sont les noeuds identiques pour tous
		for i in donnees:
			v.append(i[0][j])
		for i in range(len(v)-1):
			test=0
			if v[i]!=v[i+1]:
				test=1
				break
		if test==0:
			w.append(j)
	w.reverse()
	if len(w)>0:					   # on enleve les noeuds redondants
		for h in w:
			for j in donnees:
				j[0].pop(h)
	return donnees

# la fonction newick() prend en entree une liste dont chaque element
# contient une liste de noeuds, puis une chaine de noms de feuille
# elle retourne une chaine au format newick. La fonction est recursive
#
def newick(liste):
	nk=''
	gd=[[],[]]
	for i in liste:					# positionne un noeud dans une liste a
		if i[0][0]=='1':			# gauche si 1, droite si 2
			gd[0].append(i)
			i[0]=i[0][1:]
		elif i[0][0]=='2':
			i[0]=i[0][1:]
			gd[1].append(i)
		elif i[0][0]=='f':
			return i[1]
	for i in liste:					# occurence d'ecriture au format Newick
		nk='('+str(newick(gd[0]))+','+str(newick(gd[1]))+')'
		return nk

# la fonction unone remplace la sous-chaine 'None' par '-'
# a partir de la chaine en entree. En effet, a chaque fois
# que newick() ne renvoie rien, elle ecrit 'None' dans la string
# ce qui nuit a la lisibilite lors de l'affichage de l'arbre
#

def unone(chaine):
	a=chaine.replace('None','-')

	while a.find('(-,')!= -1:
		position_motif=a.find('(-,')
		compteur=1
		c2=0
		for i in range(position_motif+3,len(a)):
			while compteur>0:
				if a[i]=="(":
					compteur=compteur+1
				elif a[i]==")":
					compteur=compteur-1
				i=i+1
				c2=c2+1
			pos_abs=position_motif+2+c2
	 	b=list(a)
		del(b[pos_abs])
		a=''
 		for i in b:
			a=a+i
		a=a.replace('(-,','',1)
	while a.find(',-)')!= -1:
		position_motif=a.find(',-)')
		compteur=1
		c2=0
		seq=range(position_motif)
		seq.reverse()
		for i in seq:
			while compteur>0:
				if a[i]=="(":
					compteur=compteur-1
				elif a[i]==")":
					compteur=compteur+1
				i=i-1
				c2=c2+1
			pos_abs=position_motif-c2
	 	b=list(a)
		del(b[pos_abs])
		a=''
 		for i in b:
			a=a+i
 		a=a.replace(',-)','',1)
	return a

temps=time.time()
rep='/ftp/ftpdir/pub/ADE-User/data/'
fich=rep+'puces_bact_atv_'+str(temps)+'.NHX'

fs=file(fich,'w+')

result=unone(newick(brut2elabore(entry)))
fs.write(result)

print '''
<APPLET codebase="http://pbil.univ-lyon1.fr/applets"
ARCHIVE = "swing.jar, ATVjapplet.jar"
CODE = "forester/atv/ATVjapplet.class"
WIDTH = 200 HEIGHT = 50>
<PARAM NAME = url_of_tree_to_load
VALUE ="http://pbil.univ-lyon1.fr/data/
''',
print 'puces_bact_atv_'+str(temps)+'.NHX',
print '''
">
</APPLET>
'''
