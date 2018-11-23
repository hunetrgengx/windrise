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
  cursor.execute("select SUBSTR(to_char(datetime,'YYYY-MM-DD'),1,10) a,sum(fees)  手续费,regexp_matches(symbol,'[a-z]+') 单位 ,symbol from "+flc+" where direction='0'  group by symbol,a order by a desc")
  rows = pd.DataFrame(data=cursor.fetchall())
  rows.columns=['日期','手续费','单位','交易对']
  sheet1=pd.concat([sheet1,rows])
  cursor.execute("select SUBSTR(to_char(datetime,'YYYY-MM-DD'),1,10) a,sum(fees)  手续费,regexp_matches(symbol,'[a-z]+\Z') 单位 ,symbol from "+flc+" where direction='1'  group by symbol,a order by a desc")
  rows = pd.DataFrame(data=cursor.fetchall())
  rows.columns=['日期','手续费','单位','交易对']
  sheet1=pd.concat([sheet1,rows])
cursor.execute("SELECT tablename FROM pg_tables WHERE tablename NOT LIKE 'pg%' AND tablename like 'match_result%' ORDER BY tablename")
table = cursor.fetchall()
for p in range(len(table)):  #在此加新的币种交易对
   getfee(table[p][0])

cursor.close()
sheet1.index=np.arange(1,sheet1.shape[0]+1,1)
nan=sheet1.isnull()[sheet1.isnull().手续费==True].index.tolist()    #确认空值序列（index）
sheet1=sheet1.drop(nan)
sheet1.to_excel('fee2.xls') 