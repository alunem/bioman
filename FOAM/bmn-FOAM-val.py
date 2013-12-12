#!/usr/bin/env python
import argparse
from pandas import *
import numpy as np
import os
import re

parser = argparse.ArgumentParser(description="Compute some performance statistics")
parser.add_argument("HMMer2col", help="file like this: actualKO <blank> predictedKO")
parser.add_argument("-f", "--fuzzy", default = '0', help="If set to 1, consider TP a match between actualKO and predictedKO +/- 1")
parser.add_argument("-r", "--reverse", default = '0', help="If set to 1, file like this: predictedKO <blank> actualKO")
parser.add_argument("-l", "--listOfKos", default = '0', help="Optional list file that forces a set of KOs to be tested")
args = parser.parse_args()

pf = args.HMMer2col
fuzz = args.fuzzy
r = args.reverse
l = args.listOfKos


def main():
        pairFile = open(pf)
	pl = pairFile.readlines()
	pairFile.close()
	if l==0:
		isSL='1'
		singleFile=open(l)
		sl = singleFile.readlines()
		singleFile.close()
		initConf=prepConfMatrix(sl,isSL)
		conf=fillConfMatrixSL(pl,initConf,r)
	else:
		isSL='0'
		initConf=prepConfMatrix(pl,isSL)
		conf=fillConfMatrix(pl,initConf,r)
	stats=Metrics(conf,fuzz)
	printMetrix(stats)

def Metrics(conf, fuzzy):
    cf=conf.astype('float')
    TTC=len(conf)
    TC= sum(cf.sum(0)) # total number of classifications
    if fuzzy=='1':
        sdiag1=np.append(0,np.diag(cf.ix[1:,:-1]))
        sdiag2=np.append(np.diag(cf.ix[:-1,1:]),0)
        tpi = sdiag1 + np.diag(cf) + sdiag2  # number of TP per class
        i1=tuple(range(len(cf)-1))
        i2=tuple(range(1,len(cf)))
        cf.values[i1,i2]=0
        cf.values[i2,i1]=0
    else: tpi = np.diag(cf)  # number of TP per class
    TP = sum(tpi) # total number of TP
    si = cf.sum(1)  # total number of predictions per class label in data (rows)
    ci = cf.sum(0)  # total number of predictions per predicted class (columns)
    fpi = ci - tpi  # nb of FP per class label in data (rows)
    fni = si - tpi  # nb of FN per class label in data (rows)
    #accuracy = TP / TC
    precision = np.mean(tpi/ci)
    recall = np.mean(tpi/si)
    f1 = 2*precision*recall/(precision+recall)
    metrics = {'precision':precision, 'recall':recall, 'f1':f1, 'TP':TP, 'TC':TC, 'TTC':TTC}
    return metrics

#prepare the matrix
def prepConfMatrix(pairList,isSingleList):
        kolist=[]
        if isSingleList=='1':
            for sing in pairList:
                kolist.append(sing.translate(None,"ko:KO").strip())
        else:
            for pair in pairList:
                    kopair=re.split(' |,',pair.translate(None,"ko:KO").strip())
                    for item in kopair:
                        kolist.append(item)
        kouni=sorted(set(kolist))
        conf=DataFrame(np.zeros([len(kouni),len(kouni)],dtype='int8'), columns=kouni, index=kouni)
        return conf

def prepConfMatrixOLD(pairList):
        kolist=[]
        for pair in pairList:
                kopair=re.split(' |,',pair.translate(None,"ko:KO").strip())
                for item in kopair:
                    kolist.append(item)
        kouni=sorted(set(kolist))
        conf=DataFrame(np.zeros([len(kouni),len(kouni)],dtype='int8'), columns=kouni, index=kouni)
        return conf

def fillConfMatrixSL(pairList,conf, inv):
    '''
    The pairList is a list of string with true labels (L) in pos 1 and predicted class (P) in pos 2
    by default, else, put inv = 1 in 3rd arg. SL means 'single list forced' which allows a pair to
	not be found in the initialized matrix
    '''
    for pair in pairList:
        p=pair.translate(None,"ko:KO").strip()
        if inv=='1':
            P=set(p.split()[0].split(','))
            L=set(p.split()[1].split(','))
        else:
            L=set(p.split()[0].split(','))
            P=set(p.split()[1].split(','))
        common = L & P
        if common:
            for c in common:
                try:
                    conf.ix[c,c] = int(conf.ix[c,c]) + 1
                    break
                except:
                    pass
        else:
            for l in L:
                for p in P:
                    try:
                        conf.ix[l,p] = int(conf.ix[l,p]) + 1
                        L,P=[],[]
                        break
                    except KeyError:
                        pass
    return conf


def fillConfMatrix(pairList,conf, inv):
    '''
    The pairList is a list of string with true labels (L) in pos 1 and predicted class (P) in pos 2
    by default, else, put inv = 1 in 3rd arg
    '''
    for pair in pairList:
        p=pair.translate(None,"ko:KO").strip()
        if inv=='1':
            P=set(p.split()[0].split(','))
            L=set(p.split()[1].split(','))
        else:
            L=set(p.split()[0].split(','))
            P=set(p.split()[1].split(','))
        common = L & P
        if common:
            c=common.pop()
            conf.ix[c,c] = int(conf.ix[c,c]) + 1
        else:
            l=L.pop()
            p=P.pop()
            conf.ix[l,p] = int(conf.ix[l,p]) + 1
    return conf



def printMetrix(MetrixOutput):
	print "Performance stats collected from:\t{}".format(pf)
	if fuzz=='1':
		print "(fuzzy mode activated)"
	print "Precision:\t{:.2%}".format(MetrixOutput['precision'])
	print "Recall:\t{:.2%}".format(MetrixOutput['recall'])
	print "F1-score:\t{:.2%}".format(MetrixOutput['f1'])
	print "Total number of KO tested:\t{}".format(int(MetrixOutput['TTC']))
	print "Total number of seqs classified:\t{}".format(int(MetrixOutput['TC']))
	print "Total number of TP:\t{}".format(int(MetrixOutput['TP']))
	print 



####### unused, but maybe not useless stuffs
def CleanKoPairsStr(pairList):
    CKP=[]
    for pair in pairList:
        p=pair.translate(None,"ko:KO").strip()
        ko1=set(p.split()[0].split(','))
        ko2=set(p.split()[1].split(','))
        common = ko1 & ko2
        if common:
            c=common.pop()
            CKP.append(c +'\t'+c)
        else:
            CKP.append(ko1.pop()+'\t'+ko2.pop())
    return CKP

def CleanKoPairs2L(pairList):
    ckp1=[]
    ckp2=[]
    for pair in pairList:
        p=pair.translate(None,"ko:KO").strip()
        ko1=set(p.split()[0].split(','))
        ko2=set(p.split()[1].split(','))
        common = ko1 & ko2
        if common:
            c=common.pop()
            ckp1.append(c)
            ckp2.append(c)
        else:
            ckp1.append(ko1.pop())
            ckp2.append(ko2.pop())
    return ckp1,ckp2


if __name__ == '__main__':
        main()



