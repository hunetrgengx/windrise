import requests,re
from bs4 import BeautifulSoup
import time
import pandas as pd 

mixinfo=[]
count = 0
#定义函数,用于处理每页的url，得到文章相关的网址、标题、日期
def url_deal(aurl):
    global mixinfo
    for i in range(len(aurl)):
        #正则注意事项，不能随便使用中括号和小括号[]()   
        getre = re.match(r'(.*?) class=list-recommend normal-recommend>\n<h3> <span>.*?index.html>(.*?)</a><a href=(.*?) onclick=void0 target=_blank title=(.*?)>.*?</a></span> </h3>\n<p class=list-text>.*?</p>\n<span class=list-details>(.*?)</span>\n</div>',aurl[i],re.S)
        deal  = [getre.group(2),getre.group(3),getre.group(4),getre.group(5)]
        mixinfo.append(deal)

#开始程序的主函数，定义urlbug用于记录没运行成功的页数、定义contentbug用于记录没跑成功的文章代码
urlbug=[]
contentbug=[]
j=1
while i<=2900:
    try:
        for i in range(i,2900):
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
            urlbug.append(i)
            i+=1
            j=1 


j=1
while i<=len(mixinfo):
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
            with open(r'E:\gj\研究\沐甜科技\\'+mixinfo[i][0]+'_'+re.search(r'\d\d\d\d-\d\d-\d\d',mixinfo[i][3],re.S).group()+'_'+mixinfo[i][2].replace(r'/','').replace(r'? ','')+".txt",'w',encoding='utf-8') as f:
                        f.writelines(mixinfo[i][2]+'\n'+mixinfo[i][3]+'\n'+'\n'+text) 
            print(i)    
            j=1
    except :   
        if j<6:#连续5次出错则自动跳过，并进行下一次
            print('i=',i,'出错',j,'次')    
            j+=1
            time.sleep(3)   
        elif j>=6:
            contentbug.append(i)
            i+=1
            j=1 

amix=pd.DataFrame(data=mixinfo)
aurlbug=pd.DataFrame(data=urlbug)
acontentbug=pd.DataFrame(data=contentbug)
amix.to_excel(r'E:\gj\研究\网址目录.xls')
aurlbug.to_excel(r'E:\gj\研究\错误页数.xls')
acontentbug.to_excel(r'E:\gj\研究\错误网址数.xls')

#i=342
#i=633、756/1540、2239、2384、2404/2465/2697的时候文章会出错