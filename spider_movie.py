# -*- coding:utf-8 -*-
from urllib import request,response,parse,error
import re
from bs4 import BeautifulSoup

class crawl:
    def __init__(self,url):
        self.url=url

#获取页面内容
    def getPage(self,Num):
        try:
            url=self.url+str(Num)+'?o=2'
            req=request.urlopen(url)
            return str(req.read(),encoding='utf-8')
        except error.URLError:
            return None
#获取电影信息
    def getContent(self):
        page=self.getPage(1)
        pattern_1=re.compile(r'(.*?)部相关电影')
        movie_num=re.findall(pattern_1,page)
        print('共有'+movie_num[0].strip()+'部相关电影')
        page_num=int(movie_num[0])/10+1
        print('共有%d页'%page_num)
        index=1
        while index<page_num:
            content=self.getPage(index)
            pattern_2 = re.compile(r'<h2><a target="_blank" href=(.*?)</a></h2>')
            items=re.findall(pattern_2,content)
            i=1
            for item in items:
                pattern_3=re.compile(r'"(.*?)"')
                link=re.findall(pattern_3,item)
                print('%d-%d—'%(index,i)+item.replace('<em>','').replace('</em>',''))
                self.getLink(link[0])
                i=i+1
            index=index+1
#获取下载地址
    def getLink(self,link):
        page=request.urlopen(link)
        content=str(page.read(),encoding='utf-8')
        soup=BeautifulSoup(content,'html.parser')
        print('百度云盘：')
        for i in soup.find_all('a',target='_blank',text='百度云盘'):
            print(str(i.parent).replace(str(i),'').replace('<p>','').replace('</p>',''))
            print(i.get('href'))
        print('迅雷下载：')
        for i in soup.find_all('a',target='_blank'):
            if str(i.get('href'))[0:6]=='magnet':
                print(i.string,end=':  ')
                print(i.get('href'))
            if str(i.get('href'))[0:4] == 'ed2k':
                    print(i.string, end=':  ')
                    print(i.get('href'))


url=r'http://www.dysfz.cc/'
key=str(input('输入电影名称：'))
url=url+'key/'+parse.quote(key)+'/'
find=crawl(url)
find.getContent()