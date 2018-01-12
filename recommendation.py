#!/usr/bin/env python
#encoding=utf-8

INDEX_DIR = "IndexFiles.index"

import sys, os
curpath=os.path.normpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
sys.path.append(curpath)
os.chdir(curpath)
sys.path.append("/home/SunKnight/miniconda2/lib/python2.7/site-packages/lucene")
sys.path.insert(0, "/home/SunKnight/pylucene")
reload(sys)
sys.setdefaultencoding('utf-8')
import lucene
from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version

import urllib, urllib2, json, hashlib, time

def func(user_access):
    vm_env = lucene.getVMEnv()
    vm_env.attachCurrentThread()
    # ------------ #
    STORE_DIR = "index"
    directory = SimpleFSDirectory(File(STORE_DIR))
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
    searcher = IndexSearcher(DirectoryReader.open(directory))
    # ------------ #
	
    tag = {}
    access = user_access.split()
    res = ''
    for i in access:
        b = i
        b = ''.join(b.split('/'))
        query = QueryParser(Version.LUCENE_CURRENT, "Tags", analyzer).parse(b)
        scoreDocs = searcher.search(query, 200).scoreDocs
        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)
            tags = doc.get("Tags")
            tag_list = tags.split()
            for j in tag_list:
        	    if j not in tag:
        		    tag[j] = 1
        	    else:
        		    tag[j] += 1
	tags_list = sorted(tag.items(), key = lambda item:item[1], reverse = True)
	for i in tags_list[:3]:
	    command = i[0]
        if command == '':
            return
        command = ''.join(command.split('/'))
        query = QueryParser(Version.LUCENE_CURRENT, "Tags", analyzer).parse(command)
        scoreDocs = searcher.search(query, 200).scoreDocs
        tmp = {}
        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)
            collect = doc.get("Likes")
            views = doc.get("Views")
            rate = float(collect) / float(views)
            tmp[doc.get("Page_num")] = rate
        res_list = sorted(tmp.items(), key = lambda item:item[1], reverse = True)
        count = 0
        for i in res_list:
            if i[0] not in res:
                res += i[0]
                res += ' '
                count += 1
            if count > 9:
                break	
    tmp_list = res.split()
    res = ''
    for i in tmp_list:
        query = QueryParser(Version.LUCENE_CURRENT, "Page_num", analyzer).parse(i)
        scoreDocs = searcher.search(query, 1).scoreDocs
        doc = searcher.doc(scoreDocs[0].doc)
        ch = doc.get('Page_num') + ' '
        ch += 'data/' + doc.get('Page_num') + '.jpg' + ' '
        ch += doc.get('Page_link') + ' '
        ch += doc.get('Views') + ' '
        ch += doc.get('Likes') + ' '
        tmp_alt = doc.get('Img_alt')
        tmp_alt = '_'.join(tmp_alt.split())
        ch += tmp_alt
        res += ch
        res += ' '
    del searcher
    del analyzer
    return res

#if __name__ == "__main__":
user_access = sys.argv[1]
lucene.initVM(vmargs=['-Djava.awt.headless=true'])
res = func(user_access)
print res
    

