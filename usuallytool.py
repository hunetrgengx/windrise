import requests
from bs4 import BeautifulSoup
import time
import os
import pandas as pd
import re




'''
自建模块，用于自己使用
创建者：耿洁
'''

#函数stol，用于将str格式转化为list格式，仅限于形如'[["a","b","c"],["a","b","c"]["a","b","c"]]'的转化为[['a','b','c'],['a','b','c']['a','b','c']],用于新浪接口的提取
def stol(a):
        a=a.replace(r'"','').replace(']','').split( (',['))
        a[0]=a[0].replace('[','')
        for i in range(len(a)):
            a[i]=a[i].split(',')
        return a    

'''
新浪接口网址
http://hq.sinajs.cn/list=M0 #实时数据
http://stock2.finance.sina.com.cn/futures/api/json.php/IndexService.getInnerFuturesMiniKLine5m?symbol=SR1909
http://stock2.finance.sina.com.cn/futures/api/json.php/IndexService.getInnerFuturesMiniKLine15m?symbol=SR1909
http://stock2.finance.sina.com.cn/futures/api/json.php/IndexService.getInnerFuturesMiniKLine30m?symbol=SR1909
http://stock2.finance.sina.com.cn/futures/api/json.php/IndexService.getInnerFuturesMiniKLine60m?symbol=SR1909
http://stock2.finance.sina.com.cn/futures/api/json.php/IndexService.getInnerFuturesDailyKLine?symbol=SR1909
http://stock2.finance.sina.com.cn/futures/api/json.php/IndexService.getInnerFuturesDailyKLine?symbol=SR1909
'''        
#定义直接读取日k线函数，并转化为dataframe格式
def dailykl(id):
    target='http://stock2.finance.sina.com.cn/futures/api/json.php/IndexService.getInnerFuturesDailyKLine?symbol='+id
    req = requests.get(url=target) #requests获取请求
    req.encoding = 'utf-8'        #定义encoding
    html = req.text               #取req的属性  
    df=stol(html)
    ndf=pd.DataFrame(data=df)
    return ndf    

#定义直接读取分钟K线函数，并转化为dataframe格式
def minkl(id,n):
    target='http://stock2.finance.sina.com.cn/futures/api/json.php/IndexService.getInnerFuturesMiniKLine'+n+'m?symbol='+id
    req = requests.get(url=target) #requests获取请求
    req.encoding = 'utf-8'        #定义encoding
    html = req.text               #取req的属性  
    df=stol(html)
    ndf=pd.DataFrame(data=df)
    return ndf

#定义函数，将日线图分钟k线图的dataframe格式转化为可以直接画k线图的格式
def transcandledata(dfb):
        xdfc=[]
        dfcc=dfb.reset_index(drop=True) #须将index重新设置，才不会出错
        for i in range(len(dfcc)):
            mix=[i,float(dfcc[1][i]),float(dfcc[2][i]),float(dfcc[3][i]),float(dfcc[4][i])]
            xdfc.append(mix)  
        return xdfc