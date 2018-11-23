import requests,re,datetime,xlwt,datetime
from bs4 import BeautifulSoup 
from xlrd import open_workbook
from xlutils.copy import copy

#定义getdate函数，获取系统当前日期，并将日期'2018-08-02'转换成'20180802'
def getdate(num):
    date=datetime.datetime.now().date() #获取系统当前日期
    srdate=date-datetime.timedelta(hours = 24*num) #srdate为系统日期减num为单位的日期
    srdate=str(srdate).replace('-','') #替换-为空
    return srdate  #返回srdate
  
def srdata(date):
  global a,sheet1,f  #使a,sheet1,f为全局变量
  req = requests.get(url='http://www.czce.com.cn/portal/DFSStaticFiles/Future/'+date[0:4]+'/'+date+'/FutureDataDailySR.htm') #获取req
  #req = requests.get(url='http://www.czce.com.cn/portal/exchange/'+date[0:4]+'/datadaily/'+date+'SR.htm') #新网页网址
  req.encoding = 'GBK'  #encoding为GBK,浏览器设置里可查看当前使用的encoding
  html = req.text            #
  bf = BeautifulSoup(html,'lxml')
  #texts = bf.find_all('td', class_ = 'td-noborder')   
  texts = bf.find_all('table', class_ = 'table')   
  patten=re.compile(r'>.*<')
  url1=patten.findall(str(texts))
  if len(url1)==0:
    print(date)
    return 1    
    pass
  else:
  
    b=0
    
    for i in range(14,len(url1)-28):
         if (i%14==0):
            
            
            b=1
            sheet1.write(a,0,url1[i].replace('<','').replace('>',''))
            a=a+1
         elif ((i+1)%14==0):
            sheet1.write(a-1,13,date[0:4]+'/'+date[4:6]+'/'+date[6:8])
         else:           
            b=b+1
            sheet1.write(a-1,b-1,float(url1[i].replace('.00','').replace(',','').replace('<','').replace('>','')))
    #for j in range(a-9,a):
     #     sheet1.write(j,13,date)
rexcel = open_workbook("E:\\code\\srdata.xlsx") # 用wlrd提供的方法读取一个excel文件
a= rexcel.sheets()[0].nrows # 用wlrd提供的方法获得现在已有的行数  
f = copy(rexcel) # 用xlutils提供的copy方法将xlrd的对象转化为xlwt的对象
sheet1 = f.get_sheet(0) # 用xlwt对象的方法获得要操作的sheet


#几天不来用这个
#for i in range(30):
#     a=a+1
#     date=getdate(i)
#     srdata(date)
a=a+1
i=1
date=getdate(i) 
b=srdata(date)
while b==1:
   i=i+1
   date=getdate(i)
   b=srdata(date)  

print('SR前一交易日行情已更新完毕！')
f.save("E:\\code\\srdata.xlsx")