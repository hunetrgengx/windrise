# -*- coding:UTF-8 -*-
#取期货每日行情表
#v1.0
import requests,re,datetime,xlwt,datetime
from bs4 import BeautifulSoup


if __name__ == '__main__':
    def getdate(num):
        date=datetime.datetime.now().date() 
        srdate=date-datetime.timedelta(hours = 24*num)
        srdate=str(srdate).replace('-','')
        return srdate
      
    def srdata(date):
      global a,sheet1,f
      #req = requests.get(url='http://www.czce.com.cn/portal/DFSStaticFiles/Future/'+date[0:4]+'/'+date+'/FutureDataDailySR.htm')
      req = requests.get(url='http://www.czce.com.cn/portal/exchange/'+date[0:4]+'/datadaily/'+date+'SR.htm')
      req.encoding = 'GBK'
      html = req.text           
      bf = BeautifulSoup(html,'lxml')
      #texts = bf.find_all('td', class_ = 'td-noborder')   
      texts = bf.find_all('table', class_ = 'table')   
      patten=re.compile(r'>.*<')
      url1=patten.findall(str(texts))
      if len(url1)==0:
        print(date)
        pass
      else:
      
        b=0
        
        for i in range(13,len(url1)-28):
             if ((i+1)%14==0 and i!=153):
                
                a=a+1
                b=0
                sheet1.write(a,0,url1[i].replace('<','').replace('>',''))
             else:		   
                b=b+1
                sheet1.write(a,b-1,url1[i].replace('<','').replace('>',''))
        for j in range(a-9,a):
              sheet1.write(j,13,date)
    a=0   
    f = xlwt.Workbook() #创建工作簿
    sheet1 = f.add_sheet(u'sheet1',cell_overwrite_ok=True) #创建sheet
    
    for i in range(2800,3101):
     a=a+1
     date=getdate(i)
     srdata(date)
     
      
    f.save(date+'text2221.xls')#保存文件     