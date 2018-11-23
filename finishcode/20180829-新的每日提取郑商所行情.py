#应用到知识有1、合并excel 2、request请求 3、应用到了try catch
import requests,re,datetime,xlwt
from urllib import request
import pandas as pd 


#定义getdate函数，获取系统当前日期，并将日期'2018-08-02'转换成'20180802'
def getdate(num):
    date=datetime.datetime.now().date() #获取系统当前日期
    srdate=date-datetime.timedelta(hours = 24*num) #srdate为系统日期减num为单位的日期
    srdate=str(srdate).replace('-','') #替换-为空
    return srdate  #返回srdate


def srdata(date):
  try:
     request.urlretrieve('http://www.czce.com.cn/cn/DFSStaticFiles/Future/'+date[0:4]+'/'+date+'/FutureDataDaily.xls','E:\\code\\ffe.xlsx')
     df=pd.read_excel('E:\\code\\ffe.xlsx')
     date=re.search('\d\d\d\d-\d\d-\d\d',df.columns.values[0]).group()
     date=date.replace('-','/')
     df.columns=df.ix[0] #将第一行设为行名
     df=df.drop([0]) #删除第一行
     nan=df.isnull()[df.isnull().今结算==True].index.tolist()  
     df=df.drop(nan) 
     df=df.rename(columns={'交割结算价':'日期'})
     df['日期']=date
     odf=pd.read_excel('E:\\code\\zssfuture2.xlsx')  
     pd.concat([odf,df]).to_excel('zssfuture.xlsx')
     
  except:
     return 1

i=1
date=getdate(i)
b=srdata(date)
while b==1:
  i=i+1
  date=getdate(i)
  b=srdata(date)

