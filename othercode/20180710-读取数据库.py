import xlwt,psycopg2
#读取数据库并将数据写入excel 
conn = psycopg2.connect(database="c2cdata", user="qaread",password="swerbn!gsWQg23", host="52.69.40.154", port="25431")
cursor = conn.cursor()
cursor.execute("select '净出金' as 净出金 ,SUBSTR(to_char(updatetime,'YYYYMMDD'),1,8)  a,sum(amount) from order_sell where updatetime  between '2018-06-25 00:00:29'  and '2018-07-06 00:00'  and  cus_released='t' or sys_released='t' group by SUBSTR(to_char(updatetime,'YYYYMMDD'),1,8) order by a asc")
 ## 获取SELECT返回的元组
rows = cursor.fetchall()







f = xlwt.Workbook() #创建工作簿
sheet1 = f.add_sheet(u'sheet1',cell_overwrite_ok=True) #创建sheet
for i in range(len(rows)):
         for j in range(len(rows[i])):
              print(rows[i][j])
              sheet1.write(i,j,rows[i][j])
f.save('text.xls')#保存文件
 ## 关闭游标
cursor.close()

