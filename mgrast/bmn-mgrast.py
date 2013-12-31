#!/usr/bin/env python
import collections
import argparse
import itertools
import json
import urllib2
import shutil
import urlparse
import os, sys

reload(sys)
sys.setdefaultencoding('utf-8')

parser = argparse.ArgumentParser(description="This is the bioman MG-RAST toolkit. It can show which projects have a chosen pattern in metadata, tell more about it, and download metagenomes directly once mgm ID provided")
parser.add_argument("pattern", help="a pattern to scan or a mgm ID for downloading")
parser.add_argument("-t", "--task", required=True, default = "download", choices=['download', 'scan', 'details'], help="Choose the task: you want to download, scan or ask for details about a MG-RAST project? Default is download")
parser.add_argument("-s", "--stage", default = "upload", choices=['upload', 'consensus', 'drisee', 'kmer', 'preprocess', 'dereplication', 'screen', 'genecalling', 'search', 'cluster', 'loadAWE', 'superblat', 'abundance', 'loadDB', 'done', 'all'], help="What stage of analysis should be downloaded? 'all' means everything. Default is 'upload' meaning data uploaded by the MG-RAST user.")
parser.add_argument("-v", "--verbosity", default = "mixs", choices=['minimal', 'mixs', 'metadata', 'stats', 'full'], help="Level of verbosity associated to task 'scan'. The default 'mixs' is advised to get a project id necessary to the task 'details'.")
parser.add_argument("-so", "--scanoutput", help="Scan output filename. Standard output if not given")
args = parser.parse_args()

p = args.pattern
t = args.task
s = args.stage
v = args.verbosity
o = args.scanoutput

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
        print "file", rec['file_name'], "from project mgm" + jid, "tagged as '" + stage + "', is being downloaded under directory " + jidpath + " using this url: " + rec['url']
        download(rec['url'],path=jidpath)
    return MGRec

def projectDetails(jid, verb="full"):
    """
    get project details
    """
    if jid.startswith("mgm"):
        raise NameError("You've provided a 'metagenome id' whereas a 'project id' was expected")
    elif jid.startswith("mgp"):
        jid=jid[3:]
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
        elif element=='libraries':
            print element
            for i,j in detail:
                print '\t' + i + ':\t' + j
        elif element=='samples':
            print element
            for i,j in detail:
                print '\t' + i + ':\t' + j
        else: print unicode(element) + ':\t' + unicode(detail)
    
def scanMGtab(pattern, verb=v, outfile=o):
    """
    scans all metadata associated to all MG-RAST projects
    for any keyword, and outputs project identifiers
    results are shown as a table
    """
    q = mgrast + "metagenome?metadata=" + pattern + "&verbosity="+ verb + "&limit=1000&order=id&direction=asc&match=all&status=both"
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
    header=""
    if verb=="mixs":
        header="status\tfeature\tmaterial\tproject_name\tname\tseq_method\tcollection_date\tcountry\tcreated\tbiome\tlongitude\tsequence_type\turl\tlocation\tPI_lastname\tenv_package_type\tlatitude\tproject_id\tid\tPI_firstname"
    elif verb=="minimal":
        header="status\tid\tname\tcreated"
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
        if not outfile:
            """Make a fancy output"""
            print
            print header
            for project in MGdata:
                print '\t'.join(unicode(x) for x in project)
        else:
            with open(outfile, 'w') as out:
                out.write(header + '\n')
                for project in MGdata:
                    out.write('\t'.join(unicode(x) for x in project) + '\n')
        print
        print "--------"
        print "A total of " + unicode(np) + " metagenome(s) were found."
        print "--------"
        if outfile:
            print "File '" + outfile + "' written."
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
                print "A total of " + unicode(detail) + "  metagenome projects were found:"
            else:
                print "No project was found, come back tomorrow."            

# execute the main function.
if __name__ == '__main__':
    main()
