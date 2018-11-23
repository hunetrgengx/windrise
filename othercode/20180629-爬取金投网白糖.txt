# -*- coding:UTF-8 -*-
#因为年度变化导致截取网页的格式有变，所以按照输入年份来查询。但是每次利用年份都要遍历365个日期组合，以后进行更新
#v1.0
import requests,re
from bs4 import BeautifulSoup


if __name__ == '__main__':
      req = requests.get(url='https://futures.cngold.org/sugar/list_643_all.html')
      req.encoding = 'utf-8'
      html = req.text           
      bf = BeautifulSoup(html,'lxml')
      texts = bf.find_all('div', class_ = 'history_news_content')   
      
      patten=re.compile(r'-\d\d-\d\d.*html')
      url1=patten.findall(str(texts))
      url1=sorted(set(url1),key=url1.index) # sorted output
      url2=[]
      url3=[]
      print(len(url1))
      print('请输入年份：')
      year=input()
      
     #爬取第一层网址 
for i in range(365):
      req = requests.get(url='https://futures.cngold.org/sugar/'+year+url1[i])
      req.encoding = 'utf-8'
      html = req.text           
      bf = BeautifulSoup(html,'lxml')                     
      texts = bf.find_all('ul', class_ = 'news_list pb20')   
      patten=re.compile(r'http.*html')
      url2=url2+patten.findall(str(texts))
       
      
for j in range(len(url2)):
      
      req = requests.get(url=url2[j])
      req.encoding = 'utf-8'
      html = req.text           
      bf = BeautifulSoup(html,'lxml')
      texts = bf.find_all('div', class_ = 'article')
      #如果无法读取数据，比如图表等，则进行判断
      if len(texts)==0:
        url3.append(url2[j])
      else:
        texts=texts[0].text     
        patten_article=re.compile(r'.*\n.*\n.*\n.*来源')
        article=patten_article.findall(texts)
        article=str(article).replace('\\n','').replace(' 20','  20')
        article=article.split('  ')
        date=article[1].split(' ')
        title=article[0].replace("['",'')
        
        with open('e:\\1\\'+date[0]+' '+title+".txt",'w',encoding='utf-8') as f:
               f.writelines(texts) 
               
               
with open('e:\\1\\'+'问题网址'+".txt",'w',encoding='utf-8') as f:
               f.writelines(url3)
                
   