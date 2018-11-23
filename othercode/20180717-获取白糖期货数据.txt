# -*- coding:UTF-8 -*-
#取期货每日行情表
#v1.0
import requests,re,datetime,xlwt
from bs4 import BeautifulSoup


if __name__ == '__main__':
      req = requests.get(url='http://www.czce.com.cn/portal/DFSStaticFiles/Future/2018/20180712/FutureDataDailySR.htm')
      req.encoding = 'GBK'
      html = req.text           
      bf = BeautifulSoup(html,'lxml')
      #texts = bf.find_all('td', class_ = 'td-noborder')   
      texts = bf.find_all('table', class_ = 'table')   
      
      
      patten=re.compile(r'>.*<')
      url1=patten.findall(str(texts))
     
      a=0
      
      b=0
      f = xlwt.Workbook() #创建工作簿
      sheet1 = f.add_sheet(u'sheet1',cell_overwrite_ok=True) #创建sheet
      for i in range(len(url1)):
           if ((i+1)%14==0 and i!=153):
              a=a+1
              
              b=0
              
              sheet1.write(a,0,url1[i].replace('<','').replace('>',''))
      
           else:		   
              b=b+1
                           
              
              sheet1.write(a,b-1,url1[i].replace('<','').replace('>',''))
           f.save('text.xls')#保存文件
			  
      
      
      
 

      
               
               

   