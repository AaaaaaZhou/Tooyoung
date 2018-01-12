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
import cv2

def get_d_dimensional_vector(a):
	image = cv2.imread(a)
	p = []
	for num in range(4):
		BGR = [0, 0, 0]
		left1 = num / 2 * len(image) / 2
		right1 = len(image) * (num / 2 + 1) / 2
		left2 = (num % 2) * len(image[0]) / 2
		right2 = len(image[0]) * (num % 2 + 1) / 2
		for i in range(left1, right1):
			for j in range(left2, right2):
				BGR[0] += image[i][j][0]
				BGR[1] += image[i][j][1]
				BGR[2] += image[i][j][2]
		sum = BGR[0] + BGR[1] + BGR[2]
		for k in range(3):
			BGR[k] = float(BGR[k]) / sum
			if BGR[k] >= 0.66:
				BGR[k] = 2
			elif BGR[k] < 0.33:
				BGR[k] = 0
			else:
				BGR[k] = 1
			p.append(BGR[k])

	return p

def get_vp(p):
	d = len(p)
	C = 2
	vp = ''
	for i in range(d):
		tmp = ''
		for j in range(p[i]):
			tmp += '1'
		for k in range(p[i], C):
			tmp += '0'
		vp += tmp

	return vp

def func(command):
    vm_env = lucene.getVMEnv()
    vm_env.attachCurrentThread()
    # ------------ #
    STORE_DIR = "index"
    directory = SimpleFSDirectory(File(STORE_DIR))
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
    searcher = IndexSearcher(DirectoryReader.open(directory))
    # ------------ #
    p = get_d_dimensional_vector(command)
    vp = get_vp(p)
    query = QueryParser(Version.LUCENE_CURRENT, "Vector", analyzer).parse(vp)
    scoreDocs = searcher.search(query, 200).scoreDocs

    dict1 = {}
    result = ""
    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
        rank = 0.6 * float(doc.get("Likes")) + 0.4 * float(doc.get("Views"))
        ch = doc.get('Page_num') + ' '
        ch += 'data/' + doc.get('Page_num') + '.jpg' + ' '
        ch += doc.get('Page_link') + ' '
        ch += doc.get('Views') + ' '
        ch += doc.get('Likes') + ' '
        tmp_alt = doc.get('Img_alt')
        tmp_alt = '_'.join(tmp_alt.split())
        ch += tmp_alt
        dict1[ch] = rank
    res_list = sorted(dict1.items(), key = lambda item:item[1], reverse = True)
    for i in res_list:
        result += i[0]
        result += ' '
    del searcher
    del analyzer
    return result

#if __name__ == "__main__":
content = sys.argv[1]
lucene.initVM(vmargs=['-Djava.awt.headless=true'])
res = func(content)
print res
    

