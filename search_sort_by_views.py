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

def IS_EN_WORD(tag):
    alpha = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ/@#$%&*!?.<>'
    for i in tag:
        if i not in alpha:
            return False
    return True

class YouDaoTranslate:
    def __init__(self, appKey, appSecret):
        self.url = 'https://openapi.youdao.com/api/'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36",
        }
        self.appKey = appKey
        self.appSecret = appSecret
        self.langFrom = 'auto'
        self.langTo = 'ja'

    def getUrlEncodedData(self, queryText):
        salt = str(int(round(time.time() * 1000)))
        sign_str = self.appKey + queryText + salt + self.appSecret
        sign = hashlib.md5(sign_str).hexdigest()
        payload = {
            'q': queryText,
            'from': self.langFrom,
            'to': self.langTo,
            'appKey': self.appKey,
            'salt': salt,
            'sign': sign
        }
        data = urllib.urlencode(payload)
        return data

    def parseHtml(self, html):
        data = json.loads(html)
        translationResult = data['translation']
        if isinstance(translationResult, list):
            translationResult = translationResult[0]
        if "basic" in data:
            pass
        return translationResult

    def translate(self, queryText):
        data = self.getUrlEncodedData(queryText)
        target_url = self.url + '?' + data
        request = urllib2.Request(target_url, headers=self.headers)
        response = urllib2.urlopen(request)
        translationResult = self.parseHtml(response.read())
        return translationResult


def func(command):
    vm_env = lucene.getVMEnv()
    vm_env.attachCurrentThread()
    STORE_DIR = "index"
    directory = SimpleFSDirectory(File(STORE_DIR))
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
    searcher = IndexSearcher(DirectoryReader.open(directory))
    query = QueryParser(Version.LUCENE_CURRENT, "Tags",analyzer).parse(command)
    scoreDocs = searcher.search(query, 200).scoreDocs

    dict1 = {}
    result = ""
    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
        ch = doc.get('Page_num') + ' '
        ch += 'data/' + doc.get('Page_num') + '.jpg' + ' '
        ch += doc.get('Page_link') + ' '
        ch += doc.get('Views') + ' '
        ch += doc.get('Likes') + ' '
        tmp_alt = doc.get('Img_alt')
        tmp_alt = '_'.join(tmp_alt.split())
        ch += tmp_alt
        dict1[ch] = doc.get('Views')
    res_list = sorted(dict1.items(), key = lambda item:item[1], reverse = True)
    for i in res_list:
        result += i[0]
        result += ' '
    del searcher
    del analyzer
    return result


content = sys.argv[1]
appKey = '54785b997e6c2518'
appSecret = 'yX9efFTC1LkmoZiSd80Q6VUNzQWC3tG4'
fanyi = YouDaoTranslate(appKey, appSecret)
if not IS_EN_WORD(content):
    content = fanyi.translate(content)
lucene.initVM(vmargs=['-Djava.awt.headless=true'])
res = func(content)
print res
    

