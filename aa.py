##充提币数据还有问题

import xlwt,psycopg2,datetime,requests,re,datetime,xlwt
from bs4 import BeautifulSoup 
from xlrd import open_workbook
from xlutils.copy import copy
from urllib import request
import pandas as pd
#编译语句：pyinstaller -F -w aa.py

date=datetime.datetime.now().date() 
lastweekdate=date-datetime.timedelta(hours = 24*7)
lastweekdate=str(lastweekdate)
print('sheet1')
##sheet1用户信息 
conn = psycopg2.connect(database="userdata", user="qaread",
                         password="swerbn!gsWQg23", host="52.69.40.154", port="25431")
cursor = conn.cursor()
cursor.execute("SELECT to_char(create_time,'yyyy-mm-dd') a,COUNT (1) 注册量  FROM user_info WHERE del_flag = 0  and to_char(create_time,'yyyy-mm-dd')>'" + lastweekdate+ "'  group by to_char(create_time,'yyyy-mm-dd') order by A desc")
 ## 获取SELECT返回的元组
rows = cursor.fetchall()
 
f = xlwt.Workbook() #创建工作簿
sheet1 = f.add_sheet(u'用户信息',cell_overwrite_ok=True) #创建sheet
sheet1.write(0,0,'日期')
sheet1.write(0,1,'注册量')
sheet1.write(0,2,'日期')
sheet1.write(0,3,'用户认证')
sheet1.write(0,4,'日期')
sheet1.write(0,5,'绑卡人数')

for i in range(len(rows)):
         for j in range(len(rows[i])):
              sheet1.write(i+1,j,rows[i][j])
cursor.close()

b=j
cursor = conn.cursor()
cursor.execute("SELECT SUBSTR(to_char(audit_time,'yyyy-mm-dd'),1,10) a,count(1) 审核通过量 FROM user_identity_info WHERE del_flag = 0  AND audit_state =1 and SUBSTR(to_char(audit_time,'yyyy-mm-dd'),1,10) > '" + lastweekdate+ "'  group by SUBSTR(to_char(audit_time,'yyyy-mm-dd'),1,10) order by A desc")
 ## 获取SELECT返回的元组
rows = cursor.fetchall()
for i in range(len(rows)):
         for j in range(b,len(rows[i])+b):
              sheet1.write(i+1,j+b,rows[i][j-b])
cursor.close()		
b=j
cursor = conn.cursor()
cursor.execute("select to_char(create_time,'yyyy-mm-dd') a,count(1) 绑卡人数 from user_account where account_no is not null and account_type='3'  and to_char(create_time,'yyyy-mm-dd') > '" + lastweekdate+ "'  group by to_char(create_time,'yyyy-mm-dd') order by A desc")
 ## 获取SELECT返回的元组
rows = cursor.fetchall()
for i in range(len(rows)):
         for j in range(b,len(rows[i])+b):
              sheet1.write(i+1,j+b,rows[i][j-b])
			  
cursor.close()			  


print('sheet2')
##sheet2资金净流入流出开始
conn = psycopg2.connect(database="c2cdata", user="qaread",
                         password="swerbn!gsWQg23", host="52.69.40.154", port="25431")
cursor = conn.cursor()
cursor.execute("select '净出金-法币提现' as 净出金 ,to_char(updatetime,'yyyy-mm-dd')  a,sum(amount) ,count(distinct uid) as 人数,count(oid) as 笔数 from order_sell where to_char(updatetime,'yyyy-mm-dd') > '2018-06-25'  and  cus_released='t' or sys_released='t' group by to_char(updatetime,'yyyy-mm-dd') order by a desc")
 ## 获取SELECT返回的元组
rows = cursor.fetchall()
 

sheet2 = f.add_sheet(u'法币充提币',cell_overwrite_ok=True) #创建sheet
sheet2.write(0,0,'状态')
sheet2.write(0,1,'日期')
sheet2.write(0,2,'金额')
sheet2.write(0,3,'人数')
sheet2.write(0,4,'笔数')

for i in range(len(rows)):
         for j in range(len(rows[i])):
              sheet2.write(i+1,j,rows[i][j])
a=i
 ## 关闭游标
cursor.close()


cursor = conn.cursor()
cursor.execute("select '净入金-法币充值' as 净入金,to_char(updatetime,'yyyy-mm-dd')  a,sum(amount),count(distinct uid) as 人数,count(oid) as 笔数 from order_buy where (buz_released='t' or ser_released ='t') and  to_char(updatetime,'yyyy-mm-dd') > '2018-06-25' group by a order by a desc")
 ## 获取SELECT返回的元组
rows2 = cursor.fetchall()

for i in range(a,a+len(rows2)):
         for j in range(len(rows2[i-a])):
              sheet2.write(i+3,j,rows2[i-a][j])

 ## 关闭游标
cursor.close()


print('sheet3')
##sheet3充币数据
conn = psycopg2.connect(database="t2tservice", user="qaread",
                         password="swerbn!gsWQg23", host="52.69.40.154", port="25430")
cursor = conn.cursor()
cursor.execute("SELECT cointype as 币种, to_char( create_time, 'yyyy-mm-dd-dd' ) as 充币时间, COUNT ( ID ) AS 充币笔数, count(distinct uid), SUM ( amount ) AS 充币金额 FROM withdrawcharge_op T  WHERE T.op_type = 0  AND create_time >= '" + lastweekdate+ "'  GROUP BY cointype, to_char( create_time, 'yyyy-mm-dd-dd' )  ORDER BY to_char( create_time, 'yyyy-mm-dd-dd' ),cointype")
 ## 获取SELECT返回的元组
rows = cursor.fetchall()
 

sheet2 = f.add_sheet(u'充币数据',cell_overwrite_ok=True) #创建sheet
sheet2.write(0,0,'币种')
sheet2.write(0,1,'时间')
sheet2.write(0,2,'充币笔数')
sheet2.write(0,3,'充币人数')
sheet2.write(0,4,'充币数量')

for i in range(len(rows)):
         for j in range(len(rows[i])):
              sheet2.write(i+1,j,rows[i][j])

 ## 关闭游标
cursor.close()

print('sheet4')
##sheet4提币数据
cursor = conn.cursor()
cursor.execute("SELECT cointype as 币种, to_char( update_time, 'yyyy-mm-dd-dd' ) as 提币时间, COUNT ( ID ) AS 提币笔数, COUNT ( distinct uid ) AS 人数, SUM ( amount ) AS 提币金额,small_flag 小额提笔标志 FROM withdrawcharge_op T  WHERE T.op_type = 1 and del_flag='0'  and status='10' AND update_time >= '" + lastweekdate+ "'  GROUP BY cointype, to_char( update_time, 'yyyy-mm-dd-dd' ),small_flag  ORDER BY to_char( update_time, 'yyyy-mm-dd-dd' ),cointype")
 ## 获取SELECT返回的元组
rows = cursor.fetchall()
 

sheet2 = f.add_sheet(u'提币数据',cell_overwrite_ok=True) #创建sheet
sheet2.write(0,0,'币种')
sheet2.write(0,1,'时间')
sheet2.write(0,2,'提币笔数')
sheet2.write(0,3,'提币人数')
sheet2.write(0,4,'提币数量')
sheet2.write(0,5,'小额提笔标志')

for i in range(len(rows)):
         for j in range(len(rows[i])):
              sheet2.write(i+1,j,rows[i][j])

 ## 关闭游标
cursor.close()


print('sheet5')
##sheet5币币交易汇总数据
##bz-usdt
cursor = conn.cursor()
cursor.execute("select symbol,SUBSTR(to_char(create_time,'yyyy-mm-dd'),1,10) a,sum(amount) 交易量  ,count(*) 交易笔数, count(DISTINCT uid) 交易人数 from match_result_BZ_usdt where direction = 0 and consign_id is not null and   create_time > '" + lastweekdate+ "' and uid not in ('4e3ef361-a918-4ab7-8e80-9192994efdd3','3d762c98-cc54-4d5c-b55d-a17119b768d4') group by symbol,SUBSTR(to_char(create_time,'yyyy-mm-dd'),1,10) order by A desc")
rows = cursor.fetchall()
sheet2 = f.add_sheet(u'币币交易汇总',cell_overwrite_ok=True) #创建sheet
sheet2.write(0,0,'交易对')
sheet2.write(0,1,'时间')
sheet2.write(0,2,'交易量')
sheet2.write(0,3,'交易笔数')
sheet2.write(0,4,'交易人数')

for i in range(len(rows)):
         for j in range(len(rows[i])):
              sheet2.write(i+1,j,rows[i][j])


##定义函数
def bisum(flc):
   global a,i
   a=i
   cursor = conn.cursor()
   cursor.execute("select symbol,SUBSTR(to_char(create_time,'yyyy-mm-dd'),1,10) a,sum(amount) 交易量  ,count(*) 交易笔数, count(DISTINCT uid) 交易人数 from  "+flc+"  where direction = 0 and consign_id is not null and   create_time > '" + lastweekdate+ "' and uid not in ('4e3ef361-a918-4ab7-8e80-9192994efdd3','3d762c98-cc54-4d5c-b55d-a17119b768d4') group by symbol,SUBSTR(to_char(create_time,'yyyy-mm-dd'),1,10) order by A desc")
   rows = cursor.fetchall()
   for i in range(a+2,len(rows)+a+2):
            for j in range(len(rows[i-a-2])):
                 sheet2.write(i+1,j,rows[i-a-2][j])


#币币交易汇总   
cursor.execute("SELECT tablename FROM pg_tables WHERE tablename NOT LIKE 'pg%' AND tablename like 'match_result%' ORDER BY tablename")
table = cursor.fetchall()
for p in range(len(table)):  #在此加新的币种交易对
   bisum(table[p][0])
cursor.close()   


#sheet7
conn = psycopg2.connect(database="c2cdata", user="qaread",
                         password="swerbn!gsWQg23", host="52.69.40.154", port="25431")
print('sheet7')
##sheet6法币交易明细数据
##buy
cursor = conn.cursor()
cursor.execute("select * from order_buy")
rows = cursor.fetchall()
sheet7 = f.add_sheet(u'法币交易明细',cell_overwrite_ok=True) #创建sheet
sheet7.write(0,0,'序列号')
sheet7.write(0,1,'用户id')
sheet7.write(0,2,'内部商家id')
sheet7.write(0,3,'订单uid')
sheet7.write(0,4,'币种usdt,wt')
sheet7.write(0,5,'币的数量')
sheet7.write(0,6,'单价')
sheet7.write(0,7,'总金额')
sheet7.write(0,8,'散户下单时间')
sheet7.write(0,9,'更新时间')
sheet7.write(0,10,'结束时间')
sheet7.write(0,11,'付款标志号')
sheet7.write(0,12,'用户取消订单,默认false')
sheet7.write(0,13,'用户确认付款')
sheet7.write(0,14,'用户是否可以上传,15分钟后可上传')
sheet7.write(0,15,'第一次上传,0：可以上传,-1：失败,1：成功')
sheet7.write(0,16,'第二次上传,0：可以上传,-1：失败,1：成功')
sheet7.write(0,17,'订单超时,用户不能上传')
sheet7.write(0,18,'商家,用户是否可以取消false:用户取消,商家不可取消true:用户不可取消,商家可取消')
sheet7.write(0,19,'商家是否取消')
sheet7.write(0,20,'商家确认放币')
sheet7.write(0,21,'客服是否确认申述有效')
sheet7.write(0,22,'客服是否放币')
sheet7.write(0,23,'申述有效且该订单无法放币的情况下,客服完成了申述处理：比如公司直接打钱给客户')
sheet7.write(0,24,'支付信息')
for i in range(len(rows)):
         for j in range(len(rows[i])):
              sheet7.write(i+1,j,rows[i][j])
cursor.close()


#法币卖出
a=i
cursor = conn.cursor()
cursor.execute("select * from order_sell")
rows = cursor.fetchall()
sheet7.write(a+3,0,'id')
sheet7.write(a+3,1,'用户id')
sheet7.write(a+3,2,'内部商家id')
sheet7.write(a+3,3,'币种usdt,wt')
sheet7.write(a+3,4,'币的数量')
sheet7.write(a+3,5,'币的数量')
sheet7.write(a+3,6,'单价')
sheet7.write(a+3,7,'总金额')
sheet7.write(a+3,8,'散户下单时间')
sheet7.write(a+3,9,'更新时间')
sheet7.write(a+3,10,'结束时间')
sheet7.write(a+3,11,'备注')
sheet7.write(a+3,12,'商户确认付款')
sheet7.write(a+3,13,'散户放币')
sheet7.write(a+3,14,'客服放币')
sheet7.write(a+3,15,'客服取消')
sheet7.write(a+3,16,'支付信息')

for i in range(a+3,len(rows)+a+3):
         for j in range(len(rows[i-a-3])):
              sheet7.write(i+1,j,rows[i-a-3][j])
cursor.close()


#sheet8合约
conn = psycopg2.connect(database="contractdata", user="qaread",
                         password="swerbn!gsWQg23", host="47.75.75.33", port="25433")
print('sheet8合约')
cursor = conn.cursor()
cursor.execute("select num 成交人数,已成交数量,已成交金额,日期,杠杆倍率,b.name 合约 from (select count(distinct a.account_id) num,sum(a.done_number)/2 已成交数量,sum(a.done_number*a.done_average_price)/200 已成交金额,SUBSTR(to_char(updatetime,'yyyy-mm-dd'),1,10) 日期,a.lever 杠杆倍率,a.type_id 合约类型 from contract_consignation a,contract_account b where a.account_id=b.id   and b.uid not in ('4e3ef361-a918-4ab7-8e80-9192994efdd3','3d762c98-cc54-4d5c-b55d-a17119b768d4')   and done_average_price is not null    group by SUBSTR(to_char(updatetime,'yyyy-mm-dd'),1,10),a.lever,a.type_id order by SUBSTR(to_char(updatetime,'yyyy-mm-dd'),1,10)  desc    ) a,contract_type b      where a.合约类型=b.id")
rows = cursor.fetchall()
sheet8 = f.add_sheet(u'合约交易日数据',cell_overwrite_ok=True) #创建sheet
sheet8.write(0,0,'成交人数')
sheet8.write(0,1,'成交数量')
sheet8.write(0,2,'已成交金额(美元)')
sheet8.write(0,3,'日期')
sheet8.write(0,4,'杠杆倍率')
sheet8.write(0,5,'合约')
for i in range(len(rows)):
         for j in range(len(rows[i])):
              sheet8.write(i+1,j,rows[i][j])
cursor.close()

print(date)
f.save('F:\\everydayjob\\'+str(date)+'.xls')#保存文件




print('郑商所行情结束,日期',date)



