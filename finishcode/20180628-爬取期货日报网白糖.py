# -*- coding:UTF-8 -*-
import requests,re
from bs4 import BeautifulSoup

#存在问题 1、中间过度到547左右的时候，无法正常读取，会报错，必须利用循环故意跳过才行;2、中间有部分网页无法抓取，暂未打开网页查询

#改进方向：1、将网址单独存储，并直接读取网址文件；2、将图片也保存下来，直接绘制成html进行阅读

#逻辑，先爬取网址，将网址存储成list，然后进行循环爬取


if __name__ == '__main__':
    #爬取网址、
  urlp=[]
  for i in range(99):
        #定义网址
        target ='http://app.qhrb.com.cn/?app=search&controller=index&action=search&type=all&wd=%E7%B3%96&page='+str(i)+'&order=rel'
        req = requests.get(url=target)#requests获取请求
        req.encoding = 'utf-8'        #定义encoding
        html = req.text               #取req的属性
        bf = BeautifulSoup(html,'lxml')
        texts = bf.find_all('div', class_ = 'article title')
        bd=BeautifulSoup(str(texts),'lxml')   
        url_name2 = str(bd.find_all('a')).replace('<a href=\"','').replace('\">',' ').replace('</a>,','\n').replace('</a>]','\n').replace('[http','http').replace(' http','http')
        url_name3 =re.sub(r'shtml.*\n','shtml\n',url_name2).split('\n')
        url_name3.pop()
        urlp=urlp+url_name3
        print(i)
     
    #爬取文本内容 
  for j in range(999):
        target = urlp[j]
        req = requests.get(url=target)
        req.encoding = 'utf-8'
        html = req.text           
        bf = BeautifulSoup(html,'lxml')
        texts = bf.find_all('div', class_ = 'article-content fontSizeSmall BSHARE_POP')
        time1  = bf.find_all('div', class_ = 'article-infos')#爬取较大范围
        bd = BeautifulSoup(str(time1),'lxml')
        time = bd.find_all('span', class_ = 'date')#定义较小范围，重新爬取
        texts=texts[0].text
        title=bf.find_all('h1', class_ = 'article-title')
        title2=str(title[0].text).replace('/','-')
        time1=str(time).replace('[<span class=\"date\">','').replace('</span>]','')
        
        print(j)
        s=requests.session()
        s.keep_alive =False

        with open('e:\\2\\'+time1[:10]+' '+title2+".txt",'w',encoding='utf-8') as f:
               f.writelines(title2+'\n'+time[0].text+'\n'+target+'\n'+texts) 

        target = urlp[j]
        req = requests.get(url=target)
        req.encoding = 'utf-8'
        html = req.text           
        bf = BeautifulSoup(html,'lxml')
        texts = bf.find_all('div', class_ = 'article-content fontSizeSmall BSHARE_POP')
        time1  = bf.find_all('div', class_ = 'article-infos')#爬取较大范围
        bd = BeautifulSoup(str(time1),'lxml')
        time = bd.find_all('span', class_ = 'date')#定义较小范围，重新爬取
        texts=texts[0].text
        title=bf.find_all('h1', class_ = 'article-title')
        title2=str(title[0].text).replace('/','-')
        time1=str(time).replace('[<span class=\"date\">','').replace('</span>]','')
        
        print(j)
        s=requests.session()
        s.keep_alive =False

        with open('e:\\1\\'+time1[:10]+' '+title2+".txt",'w',encoding='utf-8') as f:
               f.writelines(title2+'\n'+'\n'+texts) 

    

    
   