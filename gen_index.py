#!/usr/bin/env python
#encoding=utf-8
import jieba

INDEX_DIR = "IndexFiles.index"

import sys, os, lucene, threading, time
from datetime import datetime

from java.io import File
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version

from BeautifulSoup import BeautifulSoup

import urllib
import urllib2
import json
import hashlib
import re
COUNT = 1
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
        self.langTo = 'auto'

    def getUrlEncodedData(self, queryText):
        '''
        将数据url编码
        :param queryText: 待翻译的文字
        :return: 返回url编码过的数据
        '''
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
        '''
        解析页面，输出翻译结果
        :param html: 翻译返回的页面内容
        :return: None
        '''
        data = json.loads(html)
        translationResult = data['translation']
        if isinstance(translationResult, list):
            translationResult = translationResult[0]
        if "basic" in data:
            pass
        return translationResult=
    def translate(self, queryText):
        data = self.getUrlEncodedData(queryText)
        target_url = self.url + '?' + data
        request = urllib2.Request(target_url, headers=self.headers)
        response = urllib2.urlopen(request) 
        translationResult = self.parseHtml(response.read())
        return translationResult


class Ticker(object):

    def __init__(self):
        self.tick = True

    def run(self):
        while self.tick:
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(1.0)


class IndexFiles(object):
    """Usage: python IndexFiles <doc_directory>"""

    def __init__(self, root, storeDir, analyzer):

        if not os.path.exists(storeDir):
            os.mkdir(storeDir)

        store = SimpleFSDirectory(File(storeDir))
        analyzer = LimitTokenCountAnalyzer(analyzer, 1048576)
        config = IndexWriterConfig(Version.LUCENE_CURRENT, analyzer)
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        writer = IndexWriter(store, config)

        self.indexDocs(root, writer)
        ticker = Ticker()
        print 'commit index',
        threading.Thread(target=ticker.run).start()
        writer.commit()
        writer.close()
        ticker.tick = False
        print 'done'

    def indexDocs(self, root, writer):

        t1 = FieldType()
        t1.setIndexed(True)
        t1.setStored(True)
        t1.setTokenized(False)
        t1.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS)
        
        t2 = FieldType()
        t2.setIndexed(True)
        t2.setStored(False)
        t2.setTokenized(True)
        t2.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)
        
        '''
        # -------------------------
        f = open("index.txt")
        file_names = []
        l_lines = f.readlines()
        for i in l_lines:
            try:
		        name = i.strip().split()[1]
		        file_names.append(name)
            except Exception, e:
		        pass
        # -------------------------
        '''
        
        global COUNT
        '''
        appKey = '54785b997e6c2518'  # id
        appSecret = 'yX9efFTC1LkmoZiSd80Q6VUNzQWC3tG4'  # password
        fanyi = YouDaoTranslate(appKey, appSecret)
        '''
        for root, dirnames, filenames in os.walk(root):
            for filename in filenames: # !!!
                if not filename.endswith('.txt'):
                    continue
                print "adding", filename
                try:
                    # -------------
                    # Get page_info                
                    path = os.path.join(root, filename)
                    file = open(path)
                    tmp = {}
                    tmp['Page_num'] = file.readline().strip().split()[1]
                    Img_id = tmp['Page_num']
                    tmp['Page_link'] = file.readline().strip().split()[1]
                    tmp['Views'] = file.readline().strip().split()[1]
                    tmp['Likes'] = file.readline().strip().split()[1]
                    #tmp['Img_url'] = file.readline().strip().split()[1]
                    file.readline()# Img_url cannot be opened directly
                    tmp['Img_alt'] = file.readline().strip().split()[1]
                    file.readline()# Empty line.
                    Tags = file.readline().strip().split()
                    tmp['Vector'] = file.readline().strip().split()[1]
                    Vector = tmp['Vector']
                    file.close()
                    # -------------
                    '''
                    for i in range(len(Tags) - 1):
                        if IS_EN_WORD(Tags[i]):
                            continue
                        tag = fanyi.translate(Tags[i])
                        Tags[i] = tag
                    '''
                    str_tag = ' '.join(Tags)
                    
                    #str_tag = ' '.join(jieba.cut(str_tag))
                    doc = Document()
                    for i in tmp.keys():
                        doc.add(Field(i, tmp[i], t1))
                    doc.add(Field('Tags', str_tag, t1))
                    doc.add(Field('Tags', str_tag, t2))
                    doc.add(Field('Vector', Vector, t2))
                    doc.add(Field('ID', Img_id, t2))
                    writer.addDocument(doc)
                    print "-"*36
                    print "Count : ",COUNT
                    COUNT += 1
                    print "Tags : ",str_tag
                    print "-"*36
                except Exception, e:
                    print "Failed in indexDocs:", e

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    os.chdir('/home/az/Desktop/Project/data')
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print 'lucene', lucene.VERSION
    start = datetime.now()
    try:
        analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
        IndexFiles('html', 'index', analyzer)
        end = datetime.now()
        print end - start
    except Exception, e:
        print "Failed: ", e
        # raise e
