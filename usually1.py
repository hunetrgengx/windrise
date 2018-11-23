'''
数据库表
conn = psycopg2.connect(database="t2tservice", user="qaread",password="swerbn!gsWQg23", host="52.69.40.154", port="25430")
conn = psycopg2.connect(database="c2cdata", user="qaread",password="swerbn!gsWQg23", host="52.69.40.154", port="25431")
'''
import psycopg2,datetime,re
from urllib import request
import pandas as pd

#用户姓名，手机号，id
conn = psycopg2.connect(database="userdata", user="qaread",password="swerbn!gsWQg23", host="52.69.40.154", port="25431")
cursor = conn.cursor()
cursor.execute("select id,real_name,phone from user_info")
userinfo = pd.DataFrame(data=cursor.fetchall())
userinfo.index=userinfo[0]
cursor.close()

#计算stc的数据
conn = psycopg2.connect(database="t2tservice", user="qaread",password="swerbn!gsWQg23", host="52.69.40.154", port="25430")
cursor = conn.cursor()
cursor.execute("select uid ,sum(奖励bz) 奖励bz from ( select uid,amount,date,case when amount>100 then 100 when amount<=100 then amount end 奖励bz from ( select uid,sum(amount) amount ,to_char(create_time,'yyyy-mm-dd') date from match_result_stc_usdt  where  direction='0' and   to_char(create_time,'yyyy-mm-dd hh24:mi:ss') between '2018-10-20 14:00:00' and '2018-10-31 15:00:00'  and uid not in ('4e3ef361-a918-4ab7-8e80-9192994efdd3','3d762c98-cc54-4d5c-b55d-a17119b768d4') group by uid,date order by date desc) a  )  a group by uid order by 奖励bz desc")
middata = pd.DataFrame(data=cursor.fetchall())
middata.index=middata[0]
cursor.close()

#result=pd.concat([userinfo,middata],axis=1,join='inner')
result=pd.concat([userinfo,middata],axis=1,join_axes=[middata.index]) #行对齐，并采用middata的index进行匹配
result.to_excel('stc.xls')