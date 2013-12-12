#!/usr/bin/env python
import collections
import argparse
import itertools
import json
import urllib2
import shutil
import urlparse
import os, sys

parser = argparse.ArgumentParser(description="This is the bioman MG-RAST toolkit. It can show which projects have a chosen pattern in metadata, tell more about it, and download metagenomes directly once mgm ID provided")
parser.add_argument("pattern", help="a pattern to scan or a mgm ID for downloading")
parser.add_argument("-t", "--task", default = "download", choices=['download', 'scan', 'details'], help="Choose the task: you want to download, scan or ask for details about a MG-RAST project? Default is download")
parser.add_argument("-s", "--stage", default = "upload", choices=['upload', 'consensus', 'drisee', 'kmer', 'preprocess', 'dereplication', 'screen', 'genecalling', 'search', 'cluster', 'loadAWE', 'superblat', 'abundance', 'loadDB', 'done', 'all'], help="What stage of analysis should be downloaded? 'all' means everything")
args = parser.parse_args()

p = args.pattern
t = args.task
s = args.stage
mgrast = "http://api.metagenomics.anl.gov/1/"

def main():
    if t=="download":
        downloadMG(p,s)
    elif t=="scan":
        scanMGtab(p)
    elif t=="details":
        projectDetails(p)

def download(url, fileName=None, path="mgdata"):
    """
    download file once url provided
    code found here: http://stackoverflow.com/questions/862173/how-to-download-a-file-using-python-in-a-smarter-way
    """
    def getFileName(url,openUrl):
        if 'Content-Disposition' in openUrl.info():
            # If the response has Content-Disposition, try to get filename from it
            cd = dict(map(
                lambda x: x.strip().split('=') if '=' in x else (x.strip(),''),
                openUrl.info()['Content-Disposition'].split(';')))
            if 'filename' in cd:
                filename = cd['filename'].strip("\"'")
                if filename: return filename
        # if no filename was found above, parse it out of the final URL.
        return os.path.basename(urlparse.urlsplit(openUrl.url)[2])

    r = urllib2.urlopen(urllib2.Request(url))
    try:
        if not os.path.isdir(path):
            os.makedirs(path)
        fileName = fileName or getFileName(url,r)
        with open(path+'/'+fileName, 'wb') as f:
            shutil.copyfileobj(r,f)
    finally:
        r.close()


def downloadMG(jid, stage="upload"):
    """
    download data
    file_type":"stats","stage_name":"done","file_name":"999.done.order.stats","url":"http://api.metagenomics.anl.gov/1/download/mgm4447943.3?file=999.9","file_id":"999.9","id":"mgm4447943.3","stage_id":"999"
    """
    if jid.startswith("mgm"):
	jid=jid[3:]
    if stage == "all":
        q = mgrast + "download/mgm" + jid
    else: q = mgrast + "download/mgm" + jid + "?stage=" + stage
    files = json.load(urllib2.urlopen(q))
    MGRec = collections.OrderedDict()
    for rec in files:
        MGRec[rec['file_name']]=rec['url']
        jidpath='mgm'+jid+'/'+'mgm'+jid+"-"+stage
        print "file", rec['file_name'], "from project mgm'" + jid, "'tagged as '" + stage + "', is being downloaded under directory" + jidpath + " using this url: " + rec['url']
        download(rec['url'],path=jidpath)
    return MGRec

def projectDetails(jid, verb="full"):
    """
    get project details
    fetch info from http://api.metagenomics.anl.gov/1/project/mgp128?verbosity=full
    
    """
    q = mgrast + "project/mgp" + jid + "?verbosity=" + verb
    try:
        pdetails = json.load(urllib2.urlopen(q))
    except urllib2.HTTPError, err:
        if err.code == 401:
            raise NameError('You need authorization')
        else:
            print "Query did not work, here is the error code:",err.code
            raise NameError('Query was not successful')
    for element, detail in pdetails.iteritems():
        if element=='metadata':
            print element
            for i,j in detail.iteritems():
                print '\t' + i + ':\t' + j
        elif element=='metagenomes':
            print element
            for i,j in detail:
                print '\t' + i + ':\t' + j
        else: print str(element) + ':\t' + str(detail)
    
def scanMGtab(pattern):
    """
    scans all metadata associated to all MG-RAST projects
    for any keyword, and outputs project identifiers
    results are shown as a table
    """
    q = mgrast + "metagenome?metadata=" + pattern + "&verbosity=minimal&limit=1000&order=id&direction=asc&match=all&status=both"
    try:
        p = json.load(urllib2.urlopen(q))
    except urllib2.HTTPError, err:
        if err.code == 401:
            raise NameError('You need authorization')
        else:
            print "Query did not work, here is the error code:",err.code
            raise NameError('Query was not successful')
    np=""
    MGdata=[]
    for element, detail in p.iteritems():
        if element=="data":
            for i in detail:
                mg=[]
                for j,k in i.iteritems():
                    mg.append(k)
                MGdata.append(mg)
        elif element=="total_count":
                np = detail
    if np>0:
        """Make a fancy output"""
        print
        print "status\tid\tname\tcreated"
        for project in MGdata:
            print '\t'.join(project)
        print
        print "--------"
        print "A total of " + str(np) + " metagenome projects were found."
        print "--------"
    else:
        print "No project was found, come back tomorrow."

# an older version with a less fancy output than scanMGtab()
def scanMG(pattern):
    """
    scans all metadata associated to all MG-RAST projects
    for any keyword, and outputs project identifiers
    """
    q = mgrast + "metagenome?metadata=" + pattern + "&verbosity=minimal&limit=1000&order=id&direction=asc&match=all&status=both"
    try:
        p = json.load(urllib2.urlopen(q))
    except urllib2.HTTPError, err:
        if err.code == 401:
            raise NameError('You need authorization')
        else:
            print "Query did not work, here is the error code:",err.code
            raise NameError('Query was not successful')
    for element, detail in p.iteritems():
        if element=="data":
            for i in detail:
                print '---'
                for j,k in i.iteritems():
                    print j + ": " + k
        elif element=="total_count":
            if detail>0:
                print "A total of " + str(detail) + "  metagenome projects were found:"
            else:
                print "No project was found, come back tomorrow."            

# execute the main function.
if __name__ == '__main__':
    main()
