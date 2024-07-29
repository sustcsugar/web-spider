# -*- coding:UTF-8 -*-
import requests,sys,time,random
from bs4 import BeautifulSoup
from urllib.parse import quote


class downloader(object):

    def __init__(self,server,target):
        self.server= server
        self.target= target
        self.names = []
        self.urls = []
        self.word = []
        self.nums=0
        self.headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36' }

    def get_chapter_url(self):
        req = requests.get(self.target,headers=self.headers)
        print('>>>>>>>> Get URL : request status_code : '+ str(req.status_code) )
        html = req.text

        bf_chapter = BeautifulSoup(html,'html.parser')
        chapterlist = bf_chapter.find('div',class_='chapterlist')
        chapters=chapterlist.find_all('a')

        self.nums = len(chapters)
        for each in chapters : 
            self.names.append(each.text)
            self.urls.append(self.server+each.get('href'))
            self.word.append(each.get('title'))

        with open('req_chapter_class.log','w',encoding='utf-8') as fp:
            for chapter in chapters : 
                fp.write(self.server+chapter.get('href') + ',\t'+ chapter.text + ',\t' + chapter.get('title') +'\n')

    def get_content(self,name,target):
        req = requests.get(target,headers=self.headers)
        print(f"{name:<50} + Status_code : {str(req.status_code)}")
        html = req.text
        texts = []
        content_bf = BeautifulSoup(html,'html.parser')
        content= content_bf.find('div',id='content')
        paras = content.find_all('p')
        for _ in paras[1:-2]:
            texts.append(_.text)
        return '\n\n'.join(texts)
    
    def write_file(self,path,name,word,text):
        with open(path, 'a', encoding='utf-8') as f:
            f.write(name + '\n\n')
            f.write(word + '\n\n')
            f.writelines(text)
            f.write('\n\n')

def download_by_url(book_name,book_url,book_index):
    dl = downloader(book_url,book_index)
    dl.get_chapter_url()

    print('开始下载:')
    for i in range(dl.nums):
        sleep_time = random.uniform(1, 3)  # 随机等待1到3秒
        time.sleep(sleep_time*0.001)
        dl.write_file(f'{book_name}.txt',dl.names[i],dl.word[i],dl.get_content(dl.names[i],dl.urls[i]))
        sys.stdout.write("  已下载:%.3f%%" %  (float(i/dl.nums)*100) + '\r')
        sys.stdout.flush()
    print('下载完成')

def book_search(keyword):
    server = 'https://www.feibzw.com'
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36' }
    encode_keyword = quote(keyword,encoding='gbk')
    queryURL   = f'https://www.feibzw.com/book/search.aspx?SearchKey={encode_keyword}&SearchClass=1&SeaButton='
    print(f'Search URL is : {queryURL}')
    query_req = requests.get(queryURL,headers=headers)
    bf_query = BeautifulSoup(query_req.text,'html.parser')
    book_info = bf_query.find('div',id='CListTitle')
    print(book_info)
    book = book_info.find('a')
    print(book)
    book_name = book.text
    book_index = book.get('href')
    book_url = book.get('href').replace('index.html','')
    print(f'book name is : {book_name},\n book_url is : {book_url},\nindex is : {server}{book_index}')
    return book_name,server+book_url,server+book_index

def search_download(search_name):
    book_name,book_url,book_index = book_search(search_name)
    download_by_url(book_name,book_url,book_index)

if __name__ == '__main__':
    search_download('长生仙游')