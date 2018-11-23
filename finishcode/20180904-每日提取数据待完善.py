import psycopg2,datetime,re
from urllib import request
import pandas as pd
#获取前七日日期变量lastweekdate
date=datetime.datetime.now().date()
aindex=[]
for i in range(7):
  aindex.append(str(date-datetime.timedelta(hours = 24*i)))
lastweekdate=aindex[6]

print('sheet1')
sheet1=pd.DataFrame(index=aindex,columns={'注册量','审核通过量','绑卡人数'})
conn = psycopg2.connect(database="userdata", user="qaread",password="swerbn!gsWQg23", host="52.69.40.154", port="25431")
cursor = conn.cursor()
##sheet1用户信息开始 
cursor.execute("SELECT SUBSTR(to_char(create_time,'YYYY-MM-DD'),1,10) a,COUNT (1) 注册量  FROM user_info WHERE del_flag = 0  and SUBSTR(to_char(create_time,'YYYY-MM-DD'),1,10) >= '" + lastweekdate+ "'  group by SUBSTR(to_char(create_time,'YYYY-MM-DD'),1,10) order by A desc")
rows = pd.DataFrame(columns={'date','a'},data=cursor.fetchall())   ## 获取SELECT返回的元组
rows.index=rows.date
sheet1.注册量=rows.a

cursor.execute("SELECT SUBSTR(to_char(audit_time,'YYYY-MM-DD'),1,10) a,count(1) 审核通过量 FROM user_identity_info WHERE del_flag = 0  AND audit_state =1 and SUBSTR(to_char(audit_time,'YYYY-MM-DD'),1,10) >= '" + lastweekdate+ "'  group by SUBSTR(to_char(audit_time,'YYYY-MM-DD'),1,10) order by A desc")
rows = pd.DataFrame(columns={'date','a'},data=cursor.fetchall())
rows.index=rows.date
sheet1.审核通过量=rows.a

cursor.execute("select SUBSTR(to_char(create_time,'YYYY-MM-DD'),1,10) a,count(1) 绑卡人数 from user_account where account_no is not null and account_type='3'  and SUBSTR(to_char(create_time,'YYYY-MM-DD'),1,10) >= '" + lastweekdate+ "'  group by SUBSTR(to_char(create_time,'YYYY-MM-DD'),1,10) order by A desc")
rows = pd.DataFrame(columns={'date','a'},data=cursor.fetchall())
rows.index=rows.date
sheet1.绑卡人数=rows.a

cursor.close() #数据库关闭

print('sheet2')
conn = psycopg2.connect(database="c2cdata", user="qaread",password="swerbn!gsWQg23", host="52.69.40.154", port="25431")
cursor = conn.cursor()

cursor.execute("select '净出金-法币提现' as 净出金 ,SUBSTR(to_char(updatetime,'YYYY-MM-DD'),1,10)  a,sum(amount) ,count(distinct uid) as 人数,count(oid) as 笔数 from order_sell where SUBSTR(to_char(updatetime,'YYYY-MM-DD'),1,10) > '2018-06-25'  and  cus_released='t' or sys_released='t' group by SUBSTR(to_char(updatetime,'YYYY-MM-DD'),1,10) order by a desc")
#sheet2=pd.DataFrame(columns={'状态','日期','金额','人数','笔数'},data=rows) 为什么会导致顺序变化
sheet2b=pd.DataFrame(data=cursor.fetchall())
sheet2b.columns=['状态','日期','金额','人数','笔数']

cursor.execute("select '净入金-法币充值' as 净入金,SUBSTR(to_char(updatetime,'YYYY-MM-DD'),1,10)  a,sum(amount),count(distinct uid) as 人数,count(oid) as 笔数 from order_buy where (buz_released='t' or ser_released ='t') and  SUBSTR(to_char(updatetime,'YYYY-MM-DD'),1,10) > '2018-06-25' group by a order by a desc")
sheet2a=pd.DataFrame(data=cursor.fetchall())
sheet2a.columns=['状态','日期','金额','人数','笔数']

sheet2=pd.concat([sheet2a,sheet2b])
cursor.close() #数据库关闭

'''
import psycopg2,datetime,re
from urllib import request
import pandas as pd
import numpy as np

print('sheet1')
conn = psycopg2.connect(database="t2tservice", user="qaread",password="swerbn!gsWQg23", host="52.69.40.154", port="25430")
cursor = conn.cursor()
sheet1=pd.DataFrame()
def getfee(flc):
  global sheet1
  cursor.execute("select SUBSTR(to_char(datetime,'YYYY-MM-DD'),1,10) a,sum(fees)  手续费,regexp_matches(symbol,'[a-z]+') 单位 ,symbol from match_result_"+flc+" where direction='0'  group by symbol,a order by a desc")
  rows = pd.DataFrame(data=cursor.fetchall())
  rows.columns=['日期','手续费','单位','交易对']
  sheet1=pd.concat([sheet1,rows])
  cursor.execute("select SUBSTR(to_char(datetime,'YYYY-MM-DD'),1,10) a,sum(fees)  手续费,regexp_matches(symbol,'[a-z]+\Z') 单位 ,symbol from match_result_"+flc+" where direction='1'  group by symbol,a order by a desc")
  rows = pd.DataFrame(data=cursor.fetchall())
  rows.columns=['日期','手续费','单位','交易对']
  sheet1=pd.concat([sheet1,rows])
for i in ('bch_btc','bch_usdt','btc_usdt','bz_usdt','eth_btc','eth_usdt','flc_usdt','jed_usdt','ltc_btc','ltc_usdt','ugi_usdt','wicc_usdt'):
  getfee(i)

cursor.close()
sheet1.index=np.arange(1,sheet1.shape[0]+1,1)
nan=sheet1.isnull()[sheet1.isnull().手续费==True].index.tolist()    #确认空值序列（index）
sheet1=sheet1.drop(nan)
sheet1.to_excel('fee.xls') 
'''