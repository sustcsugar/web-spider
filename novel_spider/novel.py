# -*- coding:UTF-8 -*-
import requests,sys,time,random
from bs4 import BeautifulSoup


class downloader(object):

    def __init__(self):
        self.server='https://www.feibzw.com/Html/26851/'
        self.target='https://www.feibzw.com/Html/26851/index.html'
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

        with open('req_chapter_class.log','w') as fp:
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
            f.write(name + '\n')
            f.write(word + '\n')
            f.writelines(text)
            f.write('\n\n')

def test_class():
    dl = downloader()
    dl.get_chapter_url()

    print('开始下载:')
    for i in range(dl.nums):
        sleep_time = random.uniform(1, 3)  # 随机等待1到3秒
        time.sleep(sleep_time*0.001)
        dl.write_file('天域丹尊.txt',dl.names[i],dl.word[i],dl.get_content(dl.names[i],dl.urls[i]))
        sys.stdout.write("  已下载:%.3f%%" %  float(i/dl.nums) + '\r')
        sys.stdout.flush()
    print('下载完成')



def test():
    server= 'https://www.feibzw.com/Html/26851/'
    url   = 'https://www.feibzw.com/Html/26851/index.html'
    req = requests.get(url)
    print('>>>>>>>> URL request status_code is : '+str(req.status_code))

    if(req.status_code == 200) :
        html = req.text

        with open('req_html.log','w') as fp:
            fp.write(html)

        bf_chapter = BeautifulSoup(html,'html.parser')
        chapterlist = bf_chapter.find('div',class_='chapterlist')
        chapters=chapterlist.find_all('a')

        with open('req_chapter.log','w') as fp:
            for chapter in chapters : 
                fp.write(server+chapter.get('href') + ',\t'+ chapter.text + ',\t' + chapter.get('title') +'\n')

        req = requests.get('https://www.feibzw.com/Html/26851/23893601.html')
        html = req.text
        content_bf = BeautifulSoup(html,'html.parser')
        texts = content_bf.find('div',id='content')
        paragraph = texts.find_all('p')
        with open('chapter_1.txt','w') as fp:
            for p in paragraph[1:-2] : 
                fp.write(p.text + '\n')
    else :
        print("No reponse")


if __name__ == '__main__':
    test_class()
    #test()