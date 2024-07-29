# -*- coding:UTF-8 -*-
import requests,sys,os
from bs4 import BeautifulSoup

class downloader(object):

    def __init__(self):
        self.server='https://www.bqkan8.com'
        self.target='https://www.bqkan8.com/1_1094/'
        self.names = []
        self.urls = []
        self.nums=0

    """
    获取下载链接
    """
    def get_download_url(self):
        req = requests.get(self.target)
        req.encoding = 'gb18030' 
        html = req.text
        div_bf = BeautifulSoup(html)
        div = div_bf.find_all('div', class_ = 'listmain')
        a_bf = BeautifulSoup(str(div[0]))
        a = a_bf.find_all('a')
        self.nums = len(a[13:])
        for each in a[13:]:
            self.names.append(each.string)
            self.urls.append(self.server+each.get('href'))

    """
    获取章节内容
    Parameters:
        target - 下载连接(string)
    Returns:
        texts - 章节内容(string)
    Modify:
        2017-09-13
    """
    def get_contents(self,target):
        req = requests.get(url = target)
        html = req.text
        bf = BeautifulSoup(html,'lxml')
        texts = bf.find_all('div',class_='showtxt')
        texts = texts[0].text.replace('\xa0'*8,'\n\n')
        return texts

    """
    函数说明:将爬取的文章内容写入文件
    Parameters:
        name - 章节名称(string)
        path - 当前路径下,小说保存名称(string)
        text - 章节内容(string)
    Returns:
        无
    Modify:
        2017-09-13
    """
    def writer(self,name,path,text):
        write_flag = True
        with open(path, 'a', encoding='utf-8') as f:
            f.write(name + '\n')
            f.writelines(text)
            f.write('\n\n')


if __name__ == '__main__':
    dl = downloader()
    dl.get_download_url()
    print('开始下载:')

    for i in range(dl.nums):
        dl.writer(dl.names[i],'一念永恒.txt',dl.get_contents(dl.urls[i]))
        sys.stdout.write("  已下载:%.3f%%" %  float(i/dl.nums) + '\r')
        sys.stdout.flush()

    print('下载完成')

