'''
数据库表
币币
conn = psycopg2.connect(database="t2tservice", user="qaread",password="swerbn!gsWQg23", host="52.69.40.154", port="25430")
法币
conn = psycopg2.connect(database="c2cdata", user="qaread",password="swerbn!gsWQg23", host="52.69.40.154", port="25431")
币猜
conn = psycopg2.connect(database="coinguess", user="qaread",password="swerbn!gsWQg23", host="47.75.75.33", port="25433")
conn = psycopg2.connect(database="contractdata", user="qaread",password="swerbn!gsWQg23", host="47.75.75.33", port="25433")
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
cursor.execute("select uid,count(*)/4 撮合成功次数 from account_journal where op_type='6'  group by uid having count(*)/4>5 order by 撮合成功次数 desc")
middata = pd.DataFrame(data=cursor.fetchall())
middata.index=middata[0]
cursor.close()

#result=pd.concat([userinfo,middata],axis=1,join='inner')
result=pd.concat([userinfo,middata],axis=1,join_axes=[middata.index]) #行对齐，并采用middata的index进行匹配
result.to_excel('0.xls')
