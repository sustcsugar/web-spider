# 爬取图片
# https://buondua.com/


import re
import requests
import os
from bs4 import BeautifulSoup

class downloader(object):

    def __init__(self):
        self.server = 'https://buondua.com/xiaoyu-vol-698-meng-xin-yue-%E6%A2%A6%E5%BF%83%E7%8E%A5-91-photos-25182'
        self.photo_nums = 0
        self.title = []
        self.page_urls = []
        self.photo_urls = []
        self.photo_names = []

    '''
    获取标题
    '''
    def get_title(self):
        req = requests.get(self.server)
        div = BeautifulSoup(req.text,'lxml')
        header = div.find_all('div',class_='article-header')
        a_bf = BeautifulSoup(str(header[0]),'lxml')
        a = a_bf.find_all('h1')
        self.title.append(a[0].text.replace(': ','-'))

    '''
    获取页码链接
    '''
    def get_page_urls(self):
        req = requests.get(self.server)
        html = req.text
        div_bf = BeautifulSoup(html,'lxml')
        div = div_bf.find_all('div', class_ = 'pagination-list')
        a_bf = BeautifulSoup(str(div[0]),'lxml')
        a = a_bf.find_all('a')
        for each in a:
            self.page_urls.append(self.server+each.get('href'))

    '''
    获取图片地址和名字
    Parameter:
        target - page的链接
    '''
    def get_image_urls(self,target):
        req = requests.get(url=target)
        div_bf = BeautifulSoup(req.text,'lxml')
        div = div_bf.find_all('div', class_='article-fulltext')
        a_bf = BeautifulSoup(str(div[0]),'lxml')
        a = a_bf.find_all('img')
        for each in a:
            self.photo_urls.append(each.get('data-src'))
            filename = re.match(r'.*\/(.*)\?',each.get('data-src'))
            self.photo_names.append(filename.group(1))

    def writer(self):
        self.photo_nums = len(self.photo_urls)
        if os.path.exists('image/'+self.title[0]):
            print('文件夹已存在,请勿重复下载')
            exit()
        else:
            os.mkdir('image/'+self.title[0])

        for i in range(len(self.photo_urls)):
            req = requests.get(self.photo_urls[i])
            content = req.content
            with open('image/'+self.title[0]+'/'+self.photo_names[i],'wb') as fp:
                fp.write(content)
            print('    下载中 {}/{}:{}        url:{}'.format(i+1,self.photo_nums,self.photo_names[i], self.photo_urls[i]) )

if __name__ == '__main__':
    dl = downloader()
    dl.server = 'https://buondua.com/fantia-coser-%E3%81%91%E3%82%93%E7%A0%94-%E3%81%91%E3%82%93%E3%81%91%E3%82%93-2020-11-114-photos-25268'
    dl.get_title()
    print('获取标题:'+dl.title[0])
    dl.get_page_urls()
    print('获取page链接成功')
    for each in dl.page_urls:
        dl.get_image_urls(each)
    print('获取photo链接成功')
    print('图片共计 {} 张'.format(len(dl.photo_urls)))
    print('开始下载图片')
    dl.writer()
    print('下载完成: {}'.format(dl.title[0]))
