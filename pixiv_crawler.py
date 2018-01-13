# -*- coding:utf-8 -*-
from BeautifulSoup import BeautifulSoup
import urllib2
import re
import urlparse
import os
import sys
# ============= #
import threading
import Queue
import time
# ============= #
#from selenium import webdriver
import requests
import random
import numpy
import cv2


class Pixiv():

    def __init__(self):
        self.base_url = 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index'
        self.login_url = 'https://accounts.pixiv.net/api/login?lang=zh'
        self.main_url = 'http://www.pixiv.net'
        self.headers = {
        'Referer': 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)''AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/63.0.3239.84 Chrome/63.0.3239.84 Safari/537.36'
        }
        self.pixiv_id = '617810985@qq.com'
        self.password = '812750'
        self.post_key = []
        self.return_to = 'http://www.pixiv.net/'
        self.load_path = './pics'
        self.ip_list = []
        self.page_num = 0
        self.img_src = ''
        self.target_url = ''
        
    def login(self):
        post_key_html = se.get(self.base_url, headers=self.headers).text
        post_key_soup = BeautifulSoup(post_key_html)
        self.post_key = post_key_soup.find('input')['value']
        data = {
        'pixiv_id': self.pixiv_id,
        'password': self.password,
        'return_to': self.return_to,
        'post_key': self.post_key
        }
        se.post(self.login_url, data=data, headers=self.headers)
        
    def download_img(self):
        title = str(self.page_num)  # 提取标题
        #src = img_info.find('img')['src']  # 提取图片位置
        src = self.img_src
        src_headers = self.headers
        src_headers['Referer'] = self.target_url  # 增加一个referer,否则会403,referer就像上面登陆一样找
        try:
            html = requests.get(src, headers=src_headers)
            img = html.content
        except:
            print('获取该图片失败')
            return False
        print('正在保存名字为: ' + title + ' 的图片')
        print type(img)
        with open(title + '.jpg', 'ab') as f:  # 图片要用b
            f.write(img)
        print('保存该图片完毕')    
    
    def work(self):
        self.login()
        self.download_img()  # 获取图片
        print('IMG_id {page} 保存完毕'.format(page=self.page_num))
        time.sleep(2)  # 防止太快被反


def valid_filename(s):
    import string
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    s = ''.join(c for c in s if c in valid_chars)
    return s


def get_page(page):
    content = ''
    # -------------------- #
    try:
        content = urllib2.urlopen(page, timeout=10).read()
        #print 'downloading page %s' % page
        time.sleep(0.5)
    except:
        #   print "Cannot open URL. Please try again."
        pass
    # -------------------- #
    return content


def add_page_to_folder(page, content, tag, des):  # 将网页存到文件夹里，将网址和对应的文件名写入index.txt中
    index_filename = 'index.txt'  # index.txt中每行是'网址 对应的文件名'
    folder = 'html'  # 存放网页的文件夹
    filename = valid_filename(page) + '.txt' # 将网址变成合法的文件名
    index = open(index_filename, 'a')
    index.write(page.encode('ascii', 'ignore') + '\t' + filename + '\n')
    index.close()
    if not os.path.exists(folder):  # 如果文件夹不存在则新建
        os.mkdir(folder)
    f = open(os.path.join(folder, filename), 'w')
    f.write(content)  # 将网页存入文件
    f.write("\n")
    for i in tag:
        f.write(i)
        f.write("\t")
    f.write('\n')
    f.write(des)
    f.close()
    

def fetch_data(soup):
    view_count = 0
    rate_count = 0
    for i in soup.findAll('section',{'class' : 'score'}):
        #print "In section class : score"
        tmp = []
        for j in i.findAll('span',{'class' : 'views'}):
            #print "Reaching data"
            ch = str(j)
            ch = ch[ch.find('>')+1:]
            ch = ch[:ch.find('<')]
            tmp.append(int(ch))
        view_count = tmp[0]
        rate_count = tmp[1]
    return view_count, rate_count


def count_RGB(img,x1,x2,y1,y2):
    R = 0.0
    G = 0.0
    B = 0.0
    for i in range(y1,y2):
        for j in range(x1,x2):
            B += img[i][j][0]
            G += img[i][j][1]
            R += img[i][j][2]
    total = B + G + R
    R /= total
    G /= total
    B /= total
    tmp = [R,G,B]
    for i in range(3):
        if tmp[i]<0.33:
            tmp[i] = 0
        elif tmp[i] >= 0.66:
            tmp[i] = 2
        else:
            tmp[i] = 1
    return tmp
            
            
def gen_des_vector(img):
    result = []
    y = len(img)
    x = len(img[0])
    tmp = []
    tmp += count_RGB(img,0,x/2,0,y/2)
    tmp += count_RGB(img,x/2,x,0,y/2)
    tmp += count_RGB(img,0,x/2,y/2,y)
    tmp += count_RGB(img,x/2,x,y/2,y)
    for i in tmp:
        if i == 0:
            result += ['0','0']
        elif i == 1:
            result += ['1','0']
        else:
            result += ['1','1']
    return ''.join(result)


def working():
    pixiv = Pixiv()
    while not q.empty():
        try:
            seed = "https://www.pixiv.net/member_illust.php?mode=medium&illust_id="
            page_num = q.get()
            #print page_num
            page = seed + str(page_num)
            content = get_page(page)
            soup = BeautifulSoup(content)
            view_count, rate_count = fetch_data(soup)
            if view_count >= 3600 and rate_count >= 210:
                img_info = "Page_num\t" + str(page_num) + "\n"
                img_info += "Page_link\t" + str(page) + "\n"
                img_info += "view_count\t" + str(view_count) + "\n" + "rate_count\t" + str(rate_count) + "\n"
                tmp_info = ""
                img_url = ""
                for i in soup.findAll('div',{'class' : 'img-container'}):
                    for j in i.findAll('img',{'src' : re.compile('')}):
                        img_url = j.get('src','')
                        img_alt = j.get('alt','')
                        tmp_info += "img_url\t" + img_url + "\n"
                        tmp_info += "img_alt\t" + img_alt + "\n"
                if tmp_info == "":
                    print "R-18"
                    continue
                tag = []
                for i in soup.findAll('ul',{'class' : 'inline-list'}):
                    for j in i.findAll('a',{'class' : 'text'}):
                        ch = str(j)
                        ch = ch[ch.find('>')+1:]
                        ch = ch[:ch.find('<')]
                        tag.append(ch)
                
                pixiv.page_num = page_num
                pixiv.target_url = page
                pixiv.img_src = img_url
                print "Into work!"
                try:
                    pixiv.work()
                except Exception,e:
                    print e
                    print "Retrying..."
                    time.sleep(5)
                    pixiv.work()
                img_info += tmp_info
                print "# ===================================== #"
                print "View_count : ",view_count
                print "Rate_count : ",rate_count
                print " Img_info  : ",img_info
                #print "   Tags    : ",tag
                print "# ===================================== #"
                img_name = str(page_num) + '.jpg'
                img = cv2.imread(img_name)
                des_vector = "des_vector\t" + gen_des_vector(img) + "\n"
                add_page_to_folder(page, img_info, tag, des_vector)
                x = len(img[0])/3
                y = len(img)/3
                new_img = cv2.resize(img,(x,y),interpolation=cv2.INTER_AREA)
                cv2.imwrite(img_name,new_img)
            else:
                print "# ===================================== #"
                print "View_count : ",view_count
                print "Rate_count : ",rate_count
                print "Not good..."
                print "# ===================================== #"
            if varLock.acquire():
                varLock.release()
            q.task_done()
        except Exception,e:
            print e
            continue
            

if __name__ == '__main__':
    se = requests.session()
    reload(sys)
    sys.setdefaultencoding('utf-8')
    if not os.path.exists('data'):
        os.mkdir('data')
    os.chdir('/home/az/Desktop/Project/data')
    
    NUM = 16
    varLock = threading.Lock()
    q = Queue.Queue()
    
    for i in range(1,68000000):#654-655,0-9,100-101,165-167
        q.put(i)

    threads = []
    for i in range(NUM):
        t = threading.Thread(target=working)
        t.setDaemon(True)
        threads.append(t)
    
    for t in threads:
        t.start()

    for t in threads:
        t.join()
