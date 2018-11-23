import psycopg2,datetime,re
from urllib import request
import pandas as pd

conn = psycopg2.connect(database="userdata", user="qaread",password="swerbn!gsWQg23", host="52.69.40.154", port="25431")
cursor = conn.cursor()
#认证情况
cursor.execute("select a.id,a.注册时间,a.real_name,a.phone,b.认证时间,b.认证情况,c.绑定时间,c.绑定情况 from ( SELECT SUBSTR(to_char(create_time,'YYYY-MM-DD hh:mm:dd'),1,20) 注册时间,real_name,phone,id FROM user_info WHERE del_flag = 0   ) a full join ( SELECT SUBSTR(to_char(audit_time,'YYYY-MM-DD hh:mm:dd'),1,20) 认证时间,user_id,case when audit_state ='1' then '认证通过'  when audit_state ='2' then '认证失败' when audit_state ='0' then '认证中'  when audit_state is null then '未审核'    end 认证情况 FROM user_identity_info WHERE del_flag = 0  ) b  on a.id=b.user_id full join  (  select SUBSTR(to_char(create_time,'YYYY-MM-DD hh:mm:dd'),1,20) 绑定时间,user_id,account_type,case when account_type='3' then '绑定银行' when account_type is null then '未绑定' when account_type='1' then '微信' when account_type='2' then '支付宝'end 绑定情况 from user_account where account_no is not null and account_type='3' ) c on b.user_id=c.user_id")
data=cursor.fetchall()
rows = pd.DataFrame(data=data)

cursor.close()
#卖出
conn = psycopg2.connect(database="c2cdata", user="qaread",password="swerbn!gsWQg23", host="52.69.40.154", port="25431")
cursor = conn.cursor()
cursor.execute("select  uid,max(updatetime) 卖出时间 from order_sell group by uid")
dataa=cursor.fetchall()
rowsa= pd.DataFrame(data=dataa)
#买入
cursor1 = conn.cursor()
cursor1.execute("select max(updatetime) 买入时间,uid from order_buy group by uid")
datab=cursor1.fetchall()
rowsb= pd.DataFrame(data=datab)

#去除空值序列
nan=rows.isnull()[rows.isnull()[0]==True].index.tolist()    #确认空值序列（index）
rows=rows.drop(nan)

rows.index=rows[0]
rowsa.index=rowsa[0]
rowsb.index=rowsb[1]






conn = psycopg2.connect(database="t2tservice", user="qaread",password="swerbn!gsWQg23", host="52.69.40.154", port="25430")
cursor = conn.cursor()
sum=[]
def binun(nun):
    global sum,cursor
    cursor.execute("select uid,max(update_time) from " + nun +" group by uid")
    data=cursor.fetchall()
    sum+=data

cursor.execute("SELECT tablename FROM pg_tables WHERE tablename NOT LIKE 'pg%' AND tablename like 'match_result%' ORDER BY tablename")
table = cursor.fetchall()
for p in range(len(table)):  #在此加新的币种交易对
   binun(table[p][0])

rowsc=pd.DataFrame(data=sum)
rowsc=rowsc.drop_duplicates([0])
rowsc.index=rowsc[0]


sheet1=pd.concat([rowsa,rowsb,rows,rowsc],axis=1,join='outer')
sheet1.to_excel('测试.xls')

