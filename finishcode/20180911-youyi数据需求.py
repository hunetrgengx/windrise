import xlwt,psycopg2,datetime,requests,re,datetime,xlwt
from bs4 import BeautifulSoup 
from xlrd import open_workbook
from xlutils.copy import copy
from urllib import request
import pandas as pd

date=datetime.datetime.now().date() 
lastweekdate=date-datetime.timedelta(hours = 24*1)
lastweekdate=str(lastweekdate)
f = xlwt.Workbook() #创建工作簿
print('sheet1')
conn = psycopg2.connect(database="t2tservice", user="qaread", password="swerbn!gsWQg23", host="52.69.40.154", port="25430")
cursor = conn.cursor()
cursor.execute("select c.date,c.交易量,e.average ,c.成交金额,d.买入人数,d.买入笔数,d.卖出人数,d.卖出笔数,e.high,e.low,f.sum as 买入最大笔数,f.均价 as 买入最大笔数均价,g.sum as 卖出最大笔数,g.均价 as 卖出最大笔均价  from    (select to_char(create_time, 'yyyy-MM-dd' )  date,sum(amount) as 交易量, round(sum(price*amount)/sum(amount),8) as 均价,sum(price*amount) 成交金额,max(price) 最高价,min(price) 最低价 from match_result_stc_usdt group by date ) as c full join   (select a.date,a.买入人数,a.买入笔数,b.卖出人数,b.卖出笔数 from (select to_char( create_time, 'yyyy-MM-dd' )  date,count(distinct uid) as 买入人数 ,count(amount) as 买入笔数 from match_result_stc_usdt where direction='0' group by date) a,(select to_char( create_time, 'yyyy-MM-dd' )  date,count(distinct uid) as 卖出人数 ,count(amount) as 卖出笔数 from match_result_stc_usdt where direction='1' group by date) b where a.date=b.date order by a.date desc) as d on c.date=d.date full join   (select to_char(create_time::timestamp + '-1 day','YYYY-MM-DD') date,high,low ,average  from kline_day_result where symbol='stc-usdt'  ) as e  on d.date=e.date full join (select date,sum,均价 from ( select to_char(datetime,'yyyy-mm-dd') date,consign_id,sum(amount) sum,round(sum(amount*price)/sum(amount),8) 均价  ,ROW_NUMBER() over(partition by to_char(datetime,'yyyy-mm-dd') order by sum(amount) desc) as new_index from match_result_stc_usdt where direction='0' group by date,consign_id order by date desc ,sum desc ) d where d.new_index='1') f on c.date=f.date full join (select date,sum,均价 from ( select to_char(datetime,'yyyy-mm-dd') date,consign_id,sum(amount) sum,round(sum(amount*price)/sum(amount),8) 均价  ,ROW_NUMBER() over(partition by to_char(datetime,'yyyy-mm-dd') order by sum(amount) desc) as new_index from match_result_stc_usdt where direction='1' group by date,consign_id order by date desc ,sum desc ) d where d.new_index='1') g on c.date=g.date   order by date desc ")
 ## 获取SELECT返回的元组
rows = cursor.fetchall()

sheet1 = f.add_sheet(u'每日数据',cell_overwrite_ok=True) #创建sheet
sheet1.write(0,0,'日期')
sheet1.write(0,1,'交易量')
sheet1.write(0,2,'均价')
sheet1.write(0,3,'成交金额')
sheet1.write(0,4,'买入人数')
sheet1.write(0,5,'买入笔数')
sheet1.write(0,6,'卖出人数')
sheet1.write(0,7,'卖出笔数')
sheet1.write(0,8,'最高价')
sheet1.write(0,9,'最低价')
sheet1.write(0,10,'买入最大笔数量')
sheet1.write(0,11,'买入最大笔均价')
sheet1.write(0,12,'卖出最大笔数量')
sheet1.write(0,13,'卖出最大笔均价')
for i in range(len(rows)):
         for j in range(len(rows[i])):
              sheet1.write(i+1,j,rows[i][j])


print('sheet1')
cursor = conn.cursor()
cursor.execute("select ROW_NUMBER() over(order by sum(amount) desc),sum(amount) a,sum(amount*price),uid,to_char(datetime,'yyyy-mm-dd') date from match_result_stc_usdt where direction='0' and to_char(datetime,'yyyy-mm-dd')='"+lastweekdate+"'  group by uid,date order by  a desc limit 50")
 ## 获取SELECT返回的元组
rows = cursor.fetchall()
sheet1 = f.add_sheet(u'币币交易持仓',cell_overwrite_ok=True) #创建sheet
sheet1.write(0,0,'排名')
sheet1.write(0,1,'购买数量')
sheet1.write(0,2,'支出预估')
sheet1.write(0,3,'用户id')
sheet1.write(0,4,'日期')
sheet1.write(0,6,'排名')
sheet1.write(0,7,'出售数量')
sheet1.write(0,8,'支出预估')
sheet1.write(0,9,'用户id')
sheet1.write(0,10,'排名')
sheet1.write(0,11,'用户id')
sheet1.write(0,12,'持仓数量')
for i in range(len(rows)):
         for j in range(len(rows[i])):
              sheet1.write(i+1,j,rows[i][j])

b=3
cursor.execute("select ROW_NUMBER() over(order by sum(amount) desc),sum(amount) a,sum(amount*price),uid,to_char(datetime,'yyyy-mm-dd') date from match_result_stc_usdt where direction='1' and to_char(datetime,'yyyy-mm-dd')='"+lastweekdate+"'  group by uid,date order by  a desc limit 50")
 ## 获取SELECT返回的元组
rows = cursor.fetchall()
for i in range(len(rows)):
         for j in range(b,len(rows[i])+b):
              sheet1.write(i+1,j+b,rows[i][j-b])

b=5
cursor.execute("select ROW_NUMBER() over(order by balance desc),uid,balance from account_info where cointype='stc' order by balance desc limit 50")
 ## 获取SELECT返回的元组
rows = cursor.fetchall()
for i in range(len(rows)):
         for j in range(b,len(rows[i])+b):
              sheet1.write(i+1,j+b,rows[i][j-b])

print(date)
f.save('E:\\日常应用\\任务\\运营每日所需数据\\每日文件\\'+str(date)+'-stc.xls')#保存文件