import re
import time
from turtle import down
import requests
import os
from bs4 import BeautifulSoup



class download(object):

    def __init__(self):
        self.server = 'https://www.xiurenb.net'
        self.url = 'https://www.xiurenb.net/XiaoYu/10236.html'
        self.title = ''
        self.page_urls = []
        self.image_urls = []

    def get_title(self):
        req = requests.get(self.url)
        req.encoding = 'utf-8'
        bs = BeautifulSoup(req.text,'lxml')
        self.title = bs.h1.text

    def get_page_url(self):
        req = requests.get(url=self.url)
        req.encoding = 'uft-8'
        bs = BeautifulSoup(req.text,'lxml')
        page = bs.find_all('div',class_='page')
        a_href = BeautifulSoup(str(page[0]),'lxml')
        a = a_href.find_all('a')
        for i in range(1,len(a)-1):
            self.page_urls.append(a[i].get('href'))

    '''
    获取图片地址
    Parameter:
        target - page的链接
    '''
    def get_image_url(self,target):
        req = requests.get(url=target)
        req.encoding = 'utf-8'
        bs = BeautifulSoup(req.text,'lxml')
        img = bs.find_all('div',class_='content')
        src_list = BeautifulSoup(str(img[1]),'lxml')
        src = src_list.find_all('img')
        for each in src:
            self.image_urls.append(each.get('src'))

    def writer(self,title):
        #if os.path.exists('image/'+title):
        #    print('文件夹已存在:image/'+title)
        #else:
        #    print('创建文件夹:{}'.format(title))
        #    os.mkdir('image/'+title)

        print('开始下载image: {}'.format(title))
        for i in range(len(self.image_urls)):
            flag = os.path.exists('image/{}/{}{:03}.jpg'.format(title,title,i+1))
            if not flag:
                req_img = requests.get(url=self.server+self.image_urls[i])
                content = req_img.content
                print('正在下载:{}/{}  title:{}-{:03}.jpg    url:{}{}    time:{}'.format(i+1,len(self.image_urls),title,i+1,self.server,self.image_urls[i],time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
                with open('image/{}/{}-{:03}.jpg'.format(title,title,i+1),'wb') as fp:
                    fp.write(content)
                time.sleep(0.05)
            else:
                print('文件存在:{}/{}  title:{}    url:{}{}'.format(i+1,len(self.image_urls),title,self.server,self.image_urls[i]))
        print('下载完成: {}'.format(title))

'''
获取一页搜索结果的每一套图片的链接
para:
    target - string 任意一个搜索结果的网页链接
'''
def get_list(target):
    list_url = []
    list_description = []
    req = requests.get(url=target)
    req.encoding = 'utf-8'
    bs = BeautifulSoup(req.text,'lxml')
    node = bs.find_all('div',class_ = 'node')
    vols = BeautifulSoup(str(node[0]),'lxml')
    vol_title = vols.find_all('h2')
    for each in vol_title:
        list_url.append(each.a.get('href'))
        list_description.append(each.a.text[0:-15].replace(' ',''))
    return list_url,list_description

'''
获取搜索结果的多个页面链接
para:
    target - string: 任意一个搜索结果的网页链接
'''
def get_research_page(target):
    server = 'https://www.xiurenb.net/plus/search/index.asp'
    page_url = []
    req = requests.get(target)
    req.encoding = 'utf-8'
    bs = BeautifulSoup(req.text,'lxml')
    page = bs.find_all('div', class_='page')
    a_bs = BeautifulSoup(str(page[0]),'lxml')
    a = a_bs.find_all('a')
    for i in range(1,len(a)):
        page_url.append(server+a[i].get('href'))

    return page_url

'''
下载搜索结果的全部套图
para:
    target - string : 搜索结果页面地址
'''
def download_all_research_result(target):
    #page_url = get_research_page('https://www.xiurenb.net/plus/search/index.asp?keyword=%E8%8A%9D%E8%8A%9D&searchtype=title')
    page_url = get_research_page(target)
    count = 0
    for each in page_url:
        list_url,list_description = get_list(each)
        for i in range(len(list_url)):
            count = count+1
            if os.path.exists('image/'+list_description[i]):
                print('{:04}-文件夹已存在:image/{}    {}'.format(count,list_description[i],time.asctime(time.localtime(time.time()))))
            else:
                print('{:04}-创建文件夹:image/{}    {}'.format(count,list_description[i],time.asctime(time.localtime(time.time()))))
                os.mkdir('image/'+list_description[i])


                dl = download()

                with open('download_record.txt','a',encoding='utf-8') as record:
                    record.write('{:04}:{}\n\turl:{}\n\t下载时间:{}\n\n'.format(count,list_description[i],dl.server+list_url[i],time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
                dl.url = dl.server+list_url[i]
                
                dl.get_title()
                
                print('***********************开始处理第 {:04} 个**************************'.format(count))
                print('***********************时间 : {} **************************'.format(time.asctime(time.localtime(time.time()))))
                print('标题为:  {}'.format(dl.title))
                print('描述为:  {}'.format(list_description[i]))

                print('开始获取page地址')
                dl.get_page_url()
                print('获取page地址完成,共{}页'.format(len(dl.page_urls)))


                print()
                print('开始获取image地址')
                for each in dl.page_urls:
                    dl.get_image_url(dl.server+each)
                print('获取image地址完成,共{}张'.format(len(dl.image_urls)))

                print()
                dl.writer(list_description[i])
                print()
                print()
                print()
    
def download_one_page(target):
    dl = download()
    dl.url = target
    dl.get_title()
    if os.path.exists('image/'+dl.title):
        print('文件夹已存在:image/{}    {}'.format(dl.title,time.asctime(time.localtime(time.time()))))
    else:
        print('创建文件夹:image/{}    {}'.format(dl.title,time.asctime(time.localtime(time.time()))))
        os.mkdir('image/'+dl.title)

        with open('download_record.txt','a',encoding='utf-8') as record:
            record.write('单页下载: {}\n\turl:{}\n\t下载时间:{}\n\n'.format(dl.title,target,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        print('开始获取page地址')
        dl.get_page_url()
        print('获取page地址完成')
        print('获取image地址')
        for each in dl.page_urls:
            dl.get_image_url(dl.server+each)
        print('获取image地址完成, 共{}张\n'.format(len(dl.image_urls)))

        dl.writer(dl.title)



if __name__ == '__main__':
    #linwenwen = 'https://www.xiurenb.net/plus/search/index.asp?keyword=%E6%9E%97%E6%96%87%E6%96%87'
    #download_all_research_result(linwenwen)
    #yangchenchen = 'https://www.xiurenb.net/plus/search/index.asp?keyword=%E6%9D%A8%E6%99%A8%E6%99%A8&searchtype=title'
    #download_all_research_result(yangchenchen)
    #yuzijiang = 'https://www.xiurenb.net/plus/search/index.asp?keyword=%E9%B1%BC%E5%AD%90%E9%85%B1&searchtype=title'
    #download_all_research_result(yuzijiang)
    #qilijia = 'https://www.xiurenb.net/plus/search/index.asp?keyword=%E7%BB%AE%E9%87%8C%E5%98%89&searchtype=title'
    #download_all_research_result(qilijia)
    #luxuanxuan = 'https://www.xiurenb.net/plus/search/index.asp?keyword=%E9%99%86%E8%90%B1%E8%90%B1&searchtype=title'
    #download_all_research_result(luxuanxuan)
    #aixiaoqing = 'https://www.xiurenb.net/plus/search/index.asp?keyword=%E8%89%BE%E5%B0%8F%E9%9D%92'
    #download_all_research_result(aixiaoqing)
    #xiaomanyao = 'https://www.xiurenb.net/plus/search/index.asp?keyword=%E5%B0%8F%E8%9B%AE%E5%A6%96&searchtype=title'
    #download_all_research_result(xiaomanyao)
    #wangyuchun = 'https://www.xiurenb.net/plus/search/index.asp?keyword=%E7%8E%8B%E9%9B%A8%E7%BA%AF&searchtype=title'
    #download_all_research_result(wangyuchun)
    #shishi = 'https://www.xiurenb.net/plus/search/index.asp?keyword=%E8%AF%97%E8%AF%97&searchtype=title'
    #download_all_research_result(shishi)
    #yanmo = 'https://www.xiurenb.net/plus/search/index.asp?keyword=%E8%A8%80%E6%B2%AB&searchtype=title'
    #download_all_research_result(yanmo)
    #douniang = 'https://www.xiurenb.net/plus/search/index.asp?keyword=%E6%8A%96%E5%A8%98%E5%88%A9%E4%B8%96&searchtype=title'
    #download_all_research_result(douniang)
    linxinglan = 'https://www.xiurenb.com/plus/search/index.asp?keyword=%E6%9E%97%E6%98%9F%E9%98%91&searchtype=title'
    download_all_research_result(linxinglan)


    #wangxinyao_4673 = 'https://www.xiurenb.net/XiuRen/10279.html'
    #download_one_page(wangxinyao_4673)
    #wangxinyao_4688 = 'https://www.xiurenb.net/XiuRen/10301.html'
    #wangxinyao_733_huayu = 'https://www.xiurenb.net/XiaoYu/10313.html'
    #wangxinyao_736_huayu = 'https://www.xiurenb.net/XiaoYu/10344.html'
    #wangxinyao_4743 = 'https://www.xiurenb.net/XiuRen/10382.html'
    #wangxinyao_4748 = 'https://www.xiurenb.net/XiuRen/10390.html'
    #wangxinyao_743huayu = 'https://www.xiurenb.net/XiaoYu/10412.html'
    #download_one_page(wangxinyao_743huayu)
    #yangchenchen_4928 = 'https://www.xiurenb.com/XiuRen/10633.html'
    #download_one_page(yangchenchen_4928)
    #yangchenchen_772 = 'https://www.xiurenb.com/XiaoYu/10689.html'
    #download_one_page(yangchenchen_772)
    #ycc_768 = 'https://www.xiurenb.com/XiaoYu/10653.html'
    #download_one_page(ycc_768)
    #ycc_4928 = 'https://www.xiurenb.com/XiuRen/10633.html'
    #download_one_page(ycc_4928)
