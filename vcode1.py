import requests,re
from bs4 import BeautifulSoup
import time
import os
import pandas as pd

#创建文件夹函数
def mkdir(path):
    folder = os.path.exists(path)
    if not folder:                   #判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)            #makedirs 创建文件时如果路径不存在会创建这个路径

mixinfo=[]
count = 0
def url_deal(aurl):
    global mixinfo
    for i in range(len(aurl)):
        #正则注意事项，不能随便使用中括号和小括号[]()   
        getre = re.match(r'(.*?) class=list-recommend normal-recommend>\n<h3> <span>.*?index.html>(.*?)</a><a href=(.*?) onclick=void0 target=_blank title=(.*?)>.*?</a></span> </h3>\n<p class=list-text>.*?</p>\n<span class=list-details>(.*?)</span>\n</div>',aurl[i],re.S)
        deal  = [getre.group(2),getre.group(3),getre.group(4),getre.group(5)]
        mixinfo.append(deal)
i=0
j=1
num=10012
while i<num:
    try:
        for i in range(i,num+1):
            if i<6:
                target='http://www.msweet.com.cn/mtkj/xwzx62/c010030c-'+str(i)+'.html'
            elif i>=6:
                target ='http://www.msweet.com.cn/eportal/ui?pageId=1013961&currentPage='+str(i)+'&moduleId=e2569b5046d44d22abfa530608628071&staticRequest=yes'
            req = requests.get(url=target)#requests获取请求
            req.encoding = 'utf-8'        #定义encoding
            html = req.text               #取req的属性    
            bf = BeautifulSoup(html,'lxml')
            texts = bf.find_all('div', class_ = 'list-recommend normal-recommend')
            bd=BeautifulSoup(str(texts),'lxml') 
            nbd=str(bd).replace('<html><body><p>[</p>','').replace(r'[','').replace(r']','').replace('\'','').replace('\"','').replace('(','').replace(')','') #消除某些特殊符号，这些符号在正则中会出问题
            pt_url=re.compile(r'div class=list-recommend normal-recommend>.*?</span>\n</div>',re.S) #正则匹配式，注意.*?非贪婪模式以及最后的re.S进行匹配
            url=pt_url.findall(nbd)
            url_deal(url)
            print(i)
            j=1
    except :   
        if j<6:
            print('i=',i,'出错',j,'次')    
            j+=1
            time.sleep(3)   
        elif j>=6:
            i+=1
            j=1 
#初始化i，j，contentbug
contentbug=[]
i=0
j=1
while i<(len(mixinfo)-1):
    try:
        for i in range(i,len(mixinfo)):
            target ='http://www.msweet.com.cn/'+mixinfo[i][1]
            req = requests.get(url=target)#requests获取请求
            req.encoding = 'utf-8'        #定义encoding
            html = req.text               #取req的属性
            bf = BeautifulSoup(html,'lxml')
            texts = bf.find_all('div', class_ = 'article')
            bd=BeautifulSoup(str(texts),'lxml') 
            text=bd.text.replace('[','').replace(']','')
            mkdir(r'E:\gj\研究\沐甜科技\\'+mixinfo[i][0]) #查看是否有此文件夹，有则过，无则新建
            with open('E:\\gj\\研究\\沐甜科技\\'+mixinfo[i][0]+'\\'+mixinfo[i][0]+'_'+re.search(r'\d\d\d\d-\d\d-\d\d',mixinfo[i][3],re.S).group()+'_'+mixinfo[i][2].replace(r'/','').replace(r'? ','')+".txt",'w',encoding='utf-8') as f:
                        f.writelines(mixinfo[i][2]+'\n'+mixinfo[i][3]+'\n'+'\n'+text) 
            print(i)    
            j=1
    except :   
        if j<6:
            print('i=',i,'出错',j,'次')    
            j+=1
            time.sleep(3)   
        elif j>=6:
            bugg=[mixinfo[i][2],target,mixinfo[i][3]]
            contentbug.append(bugg)
            i+=1
            j=1 

acontentbug=pd.DataFrame(data=contentbug)
rexcel = pd.read_excel(r'E:\gj\研究\沐甜科技\错误网址.xls')
result=pd.concat([acontentbug,rexcel])
result.to_excel(r'E:\gj\研究\沐甜科技\错误网址.xls')