##充提币数据还有问题

import xlwt,psycopg2,datetime,requests,re,datetime,xlwt
from bs4 import BeautifulSoup 
from xlrd import open_workbook
from xlutils.copy import copy
from urllib import request
import pandas as pd


date=datetime.datetime.now().date() 
lastweekdate=date-datetime.timedelta(hours = 24*365)
lastweekdate=str(lastweekdate)
print('sheet1')
##sheet1用户信息 
conn = psycopg2.connect(database="userdata", user="qaread",
                         password="swerbn!gsWQg23", host="52.69.40.154", port="25431")
cursor = conn.cursor()
cursor.execute("SELECT SUBSTR(to_char(create_time,'YYYY-MM'),1,7) a,COUNT (1) 注册量  FROM user_info WHERE del_flag = 0  group by SUBSTR(to_char(create_time,'YYYY-MM'),1,7) order by A desc")
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
cursor.execute("SELECT SUBSTR(to_char(audit_time,'YYYY-MM'),1,7) a,count(1) 审核通过量 FROM user_identity_info WHERE del_flag = 0  AND audit_state =1 and SUBSTR(to_char(audit_time,'YYYY-MM'),1,7) > '" + lastweekdate+ "'  group by SUBSTR(to_char(audit_time,'YYYY-MM'),1,7) order by A desc")
 ## 获取SELECT返回的元组
rows = cursor.fetchall()
for i in range(len(rows)):
         for j in range(b,len(rows[i])+b):
              sheet1.write(i+1,j+b,rows[i][j-b])
cursor.close()		
b=j
cursor = conn.cursor()
cursor.execute("select SUBSTR(to_char(create_time,'YYYY-MM'),1,7) a,count(1) 绑卡人数 from user_account where account_no is not null and account_type='3'  and SUBSTR(to_char(create_time,'YYYY-MM'),1,7) > '" + lastweekdate+ "'  group by SUBSTR(to_char(create_time,'YYYY-MM'),1,7) order by A desc")
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
cursor.execute("select '净出金-法币提现' as 净出金 ,SUBSTR(to_char(updatetime,'YYYY-MM'),1,7)  a,sum(amount) ,count(distinct uid) as 人数,count(oid) as 笔数 from order_sell where SUBSTR(to_char(updatetime,'YYYY-MM'),1,7) > '2018-06-25'  and  cus_released='t' or sys_released='t' group by SUBSTR(to_char(updatetime,'YYYY-MM'),1,7) order by a desc")
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
cursor.execute("select '净入金-法币充值' as 净入金,SUBSTR(to_char(updatetime,'YYYY-MM'),1,7)  a,sum(amount),count(distinct uid) as 人数,count(oid) as 笔数 from order_buy where (buz_released='t' or ser_released ='t') and  SUBSTR(to_char(updatetime,'YYYY-MM'),1,7) > '2018-06-25' group by a order by a desc")
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
cursor.execute("SELECT cointype as 币种, to_char( create_time, 'yyyy-MM' ) as 充币时间, COUNT ( ID ) AS 充币笔数, count(distinct uid), SUM ( amount ) AS 充币金额 FROM withdrawcharge_op T  WHERE T.op_type = 0  AND create_time >= '" + lastweekdate+ "'  GROUP BY cointype, to_char( create_time, 'yyyy-MM' )  ORDER BY to_char( create_time, 'yyyy-MM' ),cointype")
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
cursor.execute("SELECT cointype as 币种, to_char( create_time, 'yyyy-MM' ) as 提币时间, COUNT ( ID ) AS 提币笔数, COUNT ( distinct uid ) AS 人数, SUM ( amount ) AS 提币金额 FROM withdrawcharge_op T  WHERE T.op_type = 1 and del_flag='0'  and status='10' AND create_time >= '" + lastweekdate+ "'  GROUP BY cointype, to_char( create_time, 'yyyy-MM' )  ORDER BY to_char( create_time, 'yyyy-MM' ),cointype")
 ## 获取SELECT返回的元组
rows = cursor.fetchall()
 

sheet2 = f.add_sheet(u'提币数据',cell_overwrite_ok=True) #创建sheet
sheet2.write(0,0,'币种')
sheet2.write(0,1,'时间')
sheet2.write(0,2,'提币笔数')
sheet2.write(0,3,'提币人数')
sheet2.write(0,4,'提币数量')

for i in range(len(rows)):
         for j in range(len(rows[i])):
              sheet2.write(i+1,j,rows[i][j])

 ## 关闭游标
cursor.close()


print('sheet5')
##sheet5币币交易汇总数据
##bz-usdt
cursor = conn.cursor()
cursor.execute("select symbol,SUBSTR(to_char(create_time,'YYYY-MM'),1,7) a,sum(amount) 交易量  ,count(*) 交易笔数, count(DISTINCT uid) 交易人数 from match_result_BZ_usdt where direction = 0 and consign_id is not null and   create_time > '" + lastweekdate+ "' and uid not in ('4e3ef361-a918-4ab7-8e80-9192994efdd3','3d762c98-cc54-4d5c-b55d-a17119b768d4','def51afe-b739-4e8e-9f8f-272f9a11201c','2ca998a3-7800-4bca-be00-5330c30cd446','7698daa4-8c23-4ea1-815f-62947102b3ee','0ba7d31f-1e64-49cc-ba4a-fdc9b74054a1','a0c9428a-2e3b-4278-8124-f7350681996c','1e7520e4-ac92-4a44-92c7-a6e86972c592','c0a3dc70-b424-4810-aefd-8d15ab065d4a','9016be04-5017-4176-bebd-5e0865282e9a','71cf69a3-361d-4278-b953-d022c133db1e','c53fb423-be29-45f4-954c-8fd8df3ea9a1','3b575657-a192-4775-b939-736c07043576','4915152b-507a-424d-9397-6e39921c5133','a33e7999-fd52-490e-bea1-683b9ae5c6f6','11d1e2f8-5061-41bd-8a5e-cd010b0a80a4','3db70a8f-8f35-485a-bd4a-c55c83e3c96b','ff294c74-59c9-4dc2-ac31-944d00ff1e8e','4699aedd-20c9-4863-b39c-00fc629c9129','f4a726c6-f150-4260-b0d6-291c8b512a91','47da6f33-0f27-4889-a560-542d93677640','8651385a-93cb-48ba-a1a8-9d5259171c13','b0426ae4-e3e3-45be-85cb-d21379497b69','03f173ad-1d90-4f66-8f04-539715de54ce','22a488fa-4b65-4ff9-8f2f-7a951be52314','a54998ae-8549-428b-9098-daf27bad6921','8ae7af0f-5bb5-4e16-9541-2d1c641a8a56','770eea18-ce54-41b4-abe0-87cd513619a8','ce79ebd1-1f00-42b4-987d-ac64f5d0a410','96cdcfef-a440-48a4-b99e-6cd50a1bb637','61581927-0245-4496-83c3-158ca03c3131','370456d6-b3ce-4bf6-ac9c-130fb9140055','2788876b-2ff8-4e9a-b795-935f43ef0cbe','e7784478-127b-4f12-aa92-1f844617e25d','b4ab770b-b8be-441f-a53f-49d6a970b269','3034ab7c-2d79-406e-bb66-fd1bd19b956e','eb74418e-ffe2-40f7-94ef-ba9b51df791b','b5ab020a-f2b2-43af-b1c7-522834823ad7','5b8aad5a-9131-4ea4-8c71-4d2a1d8a60d0','1133e848-9bcd-429c-a815-f4e2292d7078','ac98fada-8756-46b5-a824-9d45e9be26b6','6cf2fa87-1b04-42c0-82b5-d34166fe843f','d395ff9c-b5cb-466a-b2e8-7d13bfd18b3d','c4f58f0c-5d17-4b91-b63c-b78b1955cafb','bd265b59-0f36-468c-81ad-99e50c08f7e8','5a9df804-6f5f-4912-bdf0-b54694097614','4336e7fb-e793-4eff-9de9-6ebd3c7917c7','796ca3ab-fc32-4471-9874-48380d4085d0','b22030eb-7263-44c3-8e0d-4feba997aa93','5d91b92c-69fc-4703-af66-bcf96049bdad','72798ded-7b7f-4c14-a4f6-70abde20794c','e427c05a-8168-4003-a78a-dbb3350fed84','3a347479-bdd9-4b64-9ab7-26f1f8bb9dd9','412cc4c3-6fde-4664-8a27-6ff282385caa','a510b0f2-dffa-4c12-8d57-3db80511caac','5046c3ea-bb2b-4ffb-9dc0-2c089225c175','0c50e046-9279-4149-9390-45f4a9e33b2c','b3cc78b8-db8d-4a06-aa28-a7e2234fd6cd','7810a5d1-ca1f-4425-89ad-b33a6ee0b70e','c5a23755-5e23-4b8e-b104-5bf1c61d2965','92411fce-d480-4b0d-bc25-1e00a145212f','7feb5089-0dbc-4246-aace-acff0af90964','38d86661-233a-4c81-829f-8a3b469af2af','800699da-75f6-4261-a51e-90e6c53ec551','cb257239-622c-4295-80a5-4c3ff88bdb0a','7f4a64e3-04ab-4826-a4ec-7e79a1260e28','e4b4eaa3-9f8c-41d0-aa87-1fea949f4f72','13593cd3-3390-4710-9d3e-de809bde56f7','f12bec0e-09c4-41e7-95b8-02c940451952','9bb05690-1d7c-4af0-a094-331ac70a1559','f5f07ff4-94be-417c-b724-21502bd3b8b7','6c05ee19-f833-4e8e-af5a-138ef228eee8','c0726629-9dee-44bb-8694-3e9db60f9b7c','83fb6e53-cf17-4fe3-b2fb-17de09986376','9976fd5a-3ead-4b79-8e0a-78ee19330908','8b52bb71-fc47-41c3-a528-da350077d3ee','6d63fd04-9d4d-4eb2-bfb3-80e213009e2c','3babb192-b05a-44cb-89df-4f7573d37896','3a50f0f4-d225-4579-9fe6-0855826c69d0','1b3ed166-2a9e-41b7-a112-20aaa4d75c41','97355dab-dc24-48fb-8f43-4468fdd9709c','24642a47-29e7-4a34-9422-970bfc8db9a9','9cfc9360-45ca-4e6d-9cdb-83c0e316752f','17692fb2-0a17-48df-9464-290ef77d72c1','4d85f001-0232-47a0-b086-9b074124a41a','cb9d58be-9dbc-42bb-823b-2ece1916e86a','ae6db648-6014-4177-ac27-37780c308944','708373aa-0ce3-4691-8291-b98821626896','1913e04a-88c9-4799-8ab7-d080d31f4eaa','0fa86620-bb20-4c6c-9187-a64a160560d3','15bff877-54ff-4b85-aa01-ef2e1b319f2b','ddef06ee-b06d-4613-bde7-c09d159e0d51','0f47857d-a19c-4b82-bccb-dfcfec3bb700','1ef769bf-8b5e-4682-a3f2-8c9dd6836cb3','9f0c22dc-00e4-4035-92e5-8dbfcaf2d012','97750938-fa59-4498-8d3d-a6ca7fe85d61','81e2bb21-3c00-437e-b9a6-ece0da05ef54','bac79b13-4d6f-482c-9e85-a3a189520060','21af77dc-204a-4104-ba51-2f0b34832f1e','fbf2fdc0-00aa-4524-a902-a04a89abd7e8','149529ee-9899-4546-91e9-c6c12e7e6c6a','cfd6cbf4-2ff8-4382-b099-d5c5c5e635e0','c07a430e-01b3-4c17-909a-ee26aac74bfd','b76a7fc9-4cdd-4369-b7ba-57c2861ff326','53508eaf-d51e-4e09-9adb-cb22e10540ed','4c7791f4-8506-41b7-96cc-07ad227c0c90','4f4e54bb-19a2-4318-bfcc-fe19f3df4834','abeda263-323c-4eeb-a43c-db56682172b1','3b4e9e89-f094-44e9-b6eb-ba1f79b8d5a3','8ec10239-6867-44cc-a500-b055d9977319','9a6f23c7-17ed-4282-b041-3357bad88496','7ef7c048-e4eb-42e1-8cde-9ef17b234277','eebe9b78-7ce8-4aa0-a003-0e4d3cf4ba71','3b41079f-8aa1-42a0-92ea-51e142b62c4f','b61b1a24-cdcd-4d3c-9762-6f42c4f2e4de','aa419fa1-d6be-4c78-af7a-e835a97154e8','55f972b1-8700-4073-82dc-f180576207f8','cb029ac6-b6fc-44d5-a853-64807f359604','49c0193b-949e-42fb-a119-cebf448d78b1','4c7eb9d3-4893-4c73-bafa-2c49f44cb838','67cca817-1244-47ee-bcd8-ed7ae61e5098','b484825a-eccf-4924-899d-e76010e52f94','bcbf710f-47cb-4b66-bfd5-80fc02ac4997','b88b616c-1dd1-4fcd-9a9b-4aa266f088d8','cdb4e6d6-2e18-4f08-a710-0cda40fb1097','4837e730-3617-40f7-a7ff-8d5ceaefaee5','c69035a8-a7ef-43ef-bb8b-55752851e1c7','71f065cf-f795-4631-8714-d700266f589a','da26b4c6-177b-40e5-b674-57ce64974b7e','dadcda57-bba8-4e02-bee3-011690115fc3','d6ee3e0e-6a0f-429d-bf78-a32074b5e40d','4537a23a-126f-4882-8667-2b48437c4861','9ac63e88-9820-40f6-bd9c-78067095fe46','277a1219-1ade-4270-a18d-52187005aaaa','4e847ead-d87c-4b36-87a9-17406804b2a9','7ee6e26a-5206-41c0-9b12-a0d28f5774f1','54bd0e8c-9dee-4625-914d-c9905a1551cc','ff1df5e5-2ff7-4c10-a25d-854d9c45e1f9','5b0f35c7-fb98-4adb-922f-09f132832680','b943a3e3-4382-4073-8dc4-8f8597626ef5','54305701-25fb-4b59-8cb7-f0cb17829fec','9f455fe1-15d8-4b98-87e3-d48d10ba60dc','c7f3a362-0d49-4d03-b86f-6ae10b36fa4d','c2d34e4e-e53b-4aae-a6fc-4e19b0df5b52','2555edcc-2a3f-4817-abce-69850a6ee599','0b4a54b1-2cf4-4733-b501-4e5489b2ad96','a6bcfc50-7f33-4066-8b82-20d80382030c','8723494e-1a0f-4760-9ad7-78b3e6ff9290','5239e0c9-9e13-4fd6-981b-d0d14fca7b33','27abaeb0-0654-4dec-bffe-65fd8fe4d183','5d074783-4fcb-4ad9-8980-c827f79148c6','192df08a-0793-48d9-9bc6-3b1086162be7','89d1227a-551a-42c7-97fa-7767b60b4ff6','85de2ffe-4f9f-42b1-a710-3148cf96b27d','1e8e13af-731a-420d-b53a-dae06f99ba87','22a4ef95-69b4-45b8-af96-aef17111d87e','e1272d7d-56d6-4881-a222-398b2bd0ac85','240e9be9-94e2-4c77-8088-8a5dc513e16a','1308240c-8d9f-4c0d-b49c-6ae2d2ac566c','88f4e856-aaca-45f4-b9a4-2fa6da5a9c3b','dcfdfd8e-987f-41ab-8236-954a569614f6','ab531011-5e75-4435-8a79-7b861901c842','c918af6e-9eaa-472d-98e4-ebc07a8df4ac','a891a463-ffb8-4072-bcca-09863642008c','ec6ee845-7f7b-48b3-aca7-616649aca3b1','019782ec-b3b2-4fbd-af43-b181c33af072','48dd2d9f-4248-4b7d-ba56-8f0673847c4a','71b8c0f4-f022-4cee-bffe-7ce25f24df58','329028b7-02be-4a73-a4ad-7b918ce31f8e','ca00231b-44ff-45d9-8612-68b347f1bebb','0df64b47-cb21-413f-82f0-66dea45362e0','03010aab-7214-4bdb-b046-803f6c63bd58','2f49ce00-56f2-4e25-b8ee-bc02c2d3cb75','8411561c-7f06-4113-a47c-9faef2a413ef','81ce0e94-d7e6-433c-8f8f-1d3e6d3bea32','1c5d6930-16f5-4f19-9597-42696a07f4ef','5d66caed-6b29-4dbd-9c2a-17b7bc7f8cd9','ab37a878-c25c-4cc8-898c-bbabeb59099b','e389d8c0-6900-41da-89e5-47a0fd58040b','af07a4d2-9a2c-439c-b2a2-b9a1873c91a1','d5fed0c9-989f-4b8e-9506-f18967923209','90a23a15-98b8-45b4-bb62-fb13ec80c9cd','40ccf770-41d0-4855-9373-6e09f81b3b9f','277b39fb-ff53-4d5b-b9d0-a4c5f9bf65c4','463431c5-049e-4b19-a121-9bf8f0d89cf7','e4a41c59-da25-4b8e-95ab-dec13e480c75','7d16a6b8-9205-4cc8-9e84-88ed91101369','cd54ce46-d4b0-417a-a942-9f5b1ed1e313','42ed89a0-8398-4cc2-bc64-813191a79102','cc4080a0-26eb-4263-95bf-3c35e7e8b21a','0543b905-b410-4041-8793-31e40a5c5015','fb85a9fb-b320-4f44-ad27-27ce25dd7ea6','393fa931-99fe-42f5-8efe-93b47ac252e8','0bb9afea-0f2a-427f-a5b7-cf060f7eb19a','b319565c-a239-4f35-8bb4-ecaf88411c98','680a8dba-79b4-468b-be05-fd2da8c295e3','cb787658-0d94-4bea-91df-f921ac36acfb','e2592dfb-19d7-4079-bf86-9e58823c54be','4b8492d3-f880-4236-9ceb-6af6cfee955a','396741eb-4771-44ce-9818-2faf0dc48785','ab75226b-d1f4-4030-8c00-0db25dab9e66','fcca1a41-d0a2-4fd1-916c-ea93b1715c62','0a7a0e65-4699-4af3-b0b6-b3b7d1f9b61e','a2b9f9ca-efa6-4a0f-87ef-36b983536d7f','09e887de-785e-4492-b5c5-76453e741303','9228f0b3-594d-40aa-a309-ecb4ad91ac8a','643a1c40-da9c-408e-8e7e-acc7b116abef','e9a78007-4c5a-4f4a-9ca7-4ddbea48d5ce','d450505c-d0fe-434c-a65b-e3b6ed137936','4f703292-5654-4233-8207-a5b259286fa1','6e132a2b-ff6e-49ee-936c-c235800a3e8e','600373d6-de16-4659-8b56-71e43046615d','e23fb365-a975-45ab-8f0e-a94f720a1191','884e0dee-1e21-4694-b5e2-4b6874d89bba','caaa669b-09b3-4d48-910b-bbca8aefe34b','f7affa0b-e3a1-4d0f-8611-086f6d5ce533','cea8020b-4b5f-4488-8bc6-b7ed8831eb5a','6d7227d4-780f-4ead-b97c-ddde5c21d9cc','872f6f37-329e-41c7-b460-f470a6040df5','4d437797-b67c-453d-a007-ad50a92e7e61','e41fd9c8-6000-495b-8982-485bc58231af','65c6c3b1-7e18-4d86-8c72-06602ef4802a','1c1461eb-4b6f-4e7d-9357-e4fda235f98d','cd888a6f-e038-45f6-8ab3-962fd2915cad','caad0940-6b15-4a83-a784-75cd4bab2d00','96890af6-1d96-4133-a361-b095a71fe61a','6f6b4281-4693-40b6-b4cd-3903ae049b05','407f63e1-1e14-4634-9a46-2b55078eae2f','dbe85870-ccab-40d6-b8ea-ce2da785bfe3','906e2f96-94de-4ac0-a3a5-480fdd16c706','78661eb6-7323-44e8-b0b1-858987645490','3ae2324c-642b-4c05-8e10-2f99c6fb6101','3069ef97-f4ce-4bda-a3fc-f1fb09b45fb5','bec5dac8-65b9-4a4f-8f05-bbc04b4a693b','8ca548b1-e247-410c-8b35-a8602184fc6e','9ec5e0fe-90a8-4555-b01f-f6746cc7eadc','56bd51ee-2b59-44c1-ac6a-63526c033db4','6d142dae-497c-4a3c-9b2d-b05bb5fa8b75','a02d8dec-16f3-4f27-ad61-10f69dbde02e','d9bcbcb2-c1aa-43ac-aa43-b22d713ebf8d','3c23dd29-5e74-42ca-a143-3834719bbab4','12c6ef6b-9987-4f7a-836a-d8ebc1539499','b1602be4-58eb-47f2-8a15-2873662d3522','bbd50cba-468a-47a3-b958-29f84085c131','9fa7378f-b213-49a2-b545-89a07df0ddc8','fb3ddcaf-d335-4539-812c-48d73b279b9f','905799e4-a006-4008-af4e-e4c98b01b46e','0047ce7a-8467-4e1f-9f9c-a11344a7bb35','4bcf6756-fba5-4d00-ace2-3a68914aaedc','6850bd60-2298-4727-8151-57699662e12f','855b589c-aa90-43b3-9ff7-13d5ce2880e4','b9a4ade7-15d6-4af7-a4f2-a6b91d167f0b','35cb9e8c-32a1-47a8-a1a3-bbfcd0d926b4','74381c11-06e6-4cc9-acec-749cb4e8d825','b258c637-9be9-4c3a-813d-dd6e8ed20717','a92f60b8-1418-4de9-9786-3524ee8ab996','2384a765-4a08-4c55-9f3f-f531b9b67b72','3f2c776f-ad72-4e04-a5a9-7a7be0783da7','316eb798-e858-485d-a72f-9fcacbde5d21','4e3578b3-7f06-4dc5-a108-063a481a5972','9b74f1f0-90a4-4e9f-bd7d-3ac1bc5cd957','a49123ea-33a1-40c1-bfbe-ff9b0342f4b9','7566975a-b6c8-4fa3-983f-b77d6c64e944','82641d8f-2e3e-4603-ae81-32107ca29aac','0bb9b32a-91c5-416c-b8ff-15df930ab718','93c76552-809e-45a7-9183-4cb6f22f1471','b2e67683-7820-4d4e-bb74-8031b019db58','7037e380-4c35-4b64-bebf-216753fe701e','e9de9fa2-0b97-4d11-b6a4-0d041bb687bb','b8b4d4a7-ba34-42bc-a0d0-8dc23f824e55','ebeb3085-76e0-4bfb-837e-4ce507576f49','ceda4f6b-2e67-4a4b-9f33-77bfc22486b5','643e32f8-691b-4fc3-aaba-6514913dc32a','9b837431-1026-49ae-b712-8d63f8655f30','6f285fd5-41b6-4668-9eb4-9aee1c7e3be1','e75c3cf6-7b0e-49ef-aaf4-61818487ca8a','b3068612-101a-436c-bbd4-2a4a7fce03d3','e4f06a09-4ac7-4c96-aa6a-a40fa3320643','e48871d2-78af-4392-a011-a54b7bcbcbfa','c9b52d0c-5576-4175-b33b-e50166650f58','07524c25-fe19-4dfa-8e63-28e9ff2562c5','6ab0b168-35a4-402a-94f6-2b7c6178025e','07890e44-5d09-4827-9b82-b93622488f06','9471cffd-f76d-4814-a85c-4d67ca72752b','277c5a96-9e8c-4e9a-b78f-353513ba5b36','89abae49-6c73-4cbb-b7aa-f097a4e495a2','1fc6250f-ef15-4a46-bc27-6c00a3c1adbe','cdabd0f1-dceb-4456-bb75-666be11006ad','6ac5bde6-b0a4-4266-bd39-f1d79db29bdf','6f92d4be-a1cd-4ade-93f6-1c9642c85186','ddd17835-b103-4e50-9887-9c4736d0ba51','fe2c8c99-2a41-494f-9b26-1450eb58a7f2','c9563e1a-0604-4f43-8ee1-bd899a57fff8','a841625b-6745-4fe0-9ed9-b77061b79426','ee280ef1-774a-4164-9da9-0efc14ed4d5a','36ae3dd3-de19-4d35-93e0-5e219190a386','a2f1a1fc-4aa0-48a0-b00a-e61fae148000','af2e4365-d085-4b40-89e1-c2b4b057b8f6','25e15d0d-78f5-4254-8d49-9a7318404363','ba7155b0-e1f4-4baf-b02c-fa09e974a388','9c3df217-c519-4a25-90d6-d83eda2594d7','61619664-4fe2-4c57-9f70-c8e11e41e919') group by symbol,SUBSTR(to_char(create_time,'YYYY-MM'),1,7) order by A desc")
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
   cursor.execute("select symbol,SUBSTR(to_char(create_time,'YYYY-MM'),1,7) a,sum(amount) 交易量  ,count(*) 交易笔数, count(DISTINCT uid) 交易人数 from  "+flc+"  where direction = 0 and consign_id is not null and   create_time > '" + lastweekdate+ "' and uid not in ('4e3ef361-a918-4ab7-8e80-9192994efdd3','3d762c98-cc54-4d5c-b55d-a17119b768d4','def51afe-b739-4e8e-9f8f-272f9a11201c','2ca998a3-7800-4bca-be00-5330c30cd446','7698daa4-8c23-4ea1-815f-62947102b3ee','0ba7d31f-1e64-49cc-ba4a-fdc9b74054a1','a0c9428a-2e3b-4278-8124-f7350681996c','1e7520e4-ac92-4a44-92c7-a6e86972c592','c0a3dc70-b424-4810-aefd-8d15ab065d4a','9016be04-5017-4176-bebd-5e0865282e9a','71cf69a3-361d-4278-b953-d022c133db1e','c53fb423-be29-45f4-954c-8fd8df3ea9a1','3b575657-a192-4775-b939-736c07043576','4915152b-507a-424d-9397-6e39921c5133','a33e7999-fd52-490e-bea1-683b9ae5c6f6','11d1e2f8-5061-41bd-8a5e-cd010b0a80a4','3db70a8f-8f35-485a-bd4a-c55c83e3c96b','ff294c74-59c9-4dc2-ac31-944d00ff1e8e','4699aedd-20c9-4863-b39c-00fc629c9129','f4a726c6-f150-4260-b0d6-291c8b512a91','47da6f33-0f27-4889-a560-542d93677640','8651385a-93cb-48ba-a1a8-9d5259171c13','b0426ae4-e3e3-45be-85cb-d21379497b69','03f173ad-1d90-4f66-8f04-539715de54ce','22a488fa-4b65-4ff9-8f2f-7a951be52314','a54998ae-8549-428b-9098-daf27bad6921','8ae7af0f-5bb5-4e16-9541-2d1c641a8a56','770eea18-ce54-41b4-abe0-87cd513619a8','ce79ebd1-1f00-42b4-987d-ac64f5d0a410','96cdcfef-a440-48a4-b99e-6cd50a1bb637','61581927-0245-4496-83c3-158ca03c3131','370456d6-b3ce-4bf6-ac9c-130fb9140055','2788876b-2ff8-4e9a-b795-935f43ef0cbe','e7784478-127b-4f12-aa92-1f844617e25d','b4ab770b-b8be-441f-a53f-49d6a970b269','3034ab7c-2d79-406e-bb66-fd1bd19b956e','eb74418e-ffe2-40f7-94ef-ba9b51df791b','b5ab020a-f2b2-43af-b1c7-522834823ad7','5b8aad5a-9131-4ea4-8c71-4d2a1d8a60d0','1133e848-9bcd-429c-a815-f4e2292d7078','ac98fada-8756-46b5-a824-9d45e9be26b6','6cf2fa87-1b04-42c0-82b5-d34166fe843f','d395ff9c-b5cb-466a-b2e8-7d13bfd18b3d','c4f58f0c-5d17-4b91-b63c-b78b1955cafb','bd265b59-0f36-468c-81ad-99e50c08f7e8','5a9df804-6f5f-4912-bdf0-b54694097614','4336e7fb-e793-4eff-9de9-6ebd3c7917c7','796ca3ab-fc32-4471-9874-48380d4085d0','b22030eb-7263-44c3-8e0d-4feba997aa93','5d91b92c-69fc-4703-af66-bcf96049bdad','72798ded-7b7f-4c14-a4f6-70abde20794c','e427c05a-8168-4003-a78a-dbb3350fed84','3a347479-bdd9-4b64-9ab7-26f1f8bb9dd9','412cc4c3-6fde-4664-8a27-6ff282385caa','a510b0f2-dffa-4c12-8d57-3db80511caac','5046c3ea-bb2b-4ffb-9dc0-2c089225c175','0c50e046-9279-4149-9390-45f4a9e33b2c','b3cc78b8-db8d-4a06-aa28-a7e2234fd6cd','7810a5d1-ca1f-4425-89ad-b33a6ee0b70e','c5a23755-5e23-4b8e-b104-5bf1c61d2965','92411fce-d480-4b0d-bc25-1e00a145212f','7feb5089-0dbc-4246-aace-acff0af90964','38d86661-233a-4c81-829f-8a3b469af2af','800699da-75f6-4261-a51e-90e6c53ec551','cb257239-622c-4295-80a5-4c3ff88bdb0a','7f4a64e3-04ab-4826-a4ec-7e79a1260e28','e4b4eaa3-9f8c-41d0-aa87-1fea949f4f72','13593cd3-3390-4710-9d3e-de809bde56f7','f12bec0e-09c4-41e7-95b8-02c940451952','9bb05690-1d7c-4af0-a094-331ac70a1559','f5f07ff4-94be-417c-b724-21502bd3b8b7','6c05ee19-f833-4e8e-af5a-138ef228eee8','c0726629-9dee-44bb-8694-3e9db60f9b7c','83fb6e53-cf17-4fe3-b2fb-17de09986376','9976fd5a-3ead-4b79-8e0a-78ee19330908','8b52bb71-fc47-41c3-a528-da350077d3ee','6d63fd04-9d4d-4eb2-bfb3-80e213009e2c','3babb192-b05a-44cb-89df-4f7573d37896','3a50f0f4-d225-4579-9fe6-0855826c69d0','1b3ed166-2a9e-41b7-a112-20aaa4d75c41','97355dab-dc24-48fb-8f43-4468fdd9709c','24642a47-29e7-4a34-9422-970bfc8db9a9','9cfc9360-45ca-4e6d-9cdb-83c0e316752f','17692fb2-0a17-48df-9464-290ef77d72c1','4d85f001-0232-47a0-b086-9b074124a41a','cb9d58be-9dbc-42bb-823b-2ece1916e86a','ae6db648-6014-4177-ac27-37780c308944','708373aa-0ce3-4691-8291-b98821626896','1913e04a-88c9-4799-8ab7-d080d31f4eaa','0fa86620-bb20-4c6c-9187-a64a160560d3','15bff877-54ff-4b85-aa01-ef2e1b319f2b','ddef06ee-b06d-4613-bde7-c09d159e0d51','0f47857d-a19c-4b82-bccb-dfcfec3bb700','1ef769bf-8b5e-4682-a3f2-8c9dd6836cb3','9f0c22dc-00e4-4035-92e5-8dbfcaf2d012','97750938-fa59-4498-8d3d-a6ca7fe85d61','81e2bb21-3c00-437e-b9a6-ece0da05ef54','bac79b13-4d6f-482c-9e85-a3a189520060','21af77dc-204a-4104-ba51-2f0b34832f1e','fbf2fdc0-00aa-4524-a902-a04a89abd7e8','149529ee-9899-4546-91e9-c6c12e7e6c6a','cfd6cbf4-2ff8-4382-b099-d5c5c5e635e0','c07a430e-01b3-4c17-909a-ee26aac74bfd','b76a7fc9-4cdd-4369-b7ba-57c2861ff326','53508eaf-d51e-4e09-9adb-cb22e10540ed','4c7791f4-8506-41b7-96cc-07ad227c0c90','4f4e54bb-19a2-4318-bfcc-fe19f3df4834','abeda263-323c-4eeb-a43c-db56682172b1','3b4e9e89-f094-44e9-b6eb-ba1f79b8d5a3','8ec10239-6867-44cc-a500-b055d9977319','9a6f23c7-17ed-4282-b041-3357bad88496','7ef7c048-e4eb-42e1-8cde-9ef17b234277','eebe9b78-7ce8-4aa0-a003-0e4d3cf4ba71','3b41079f-8aa1-42a0-92ea-51e142b62c4f','b61b1a24-cdcd-4d3c-9762-6f42c4f2e4de','aa419fa1-d6be-4c78-af7a-e835a97154e8','55f972b1-8700-4073-82dc-f180576207f8','cb029ac6-b6fc-44d5-a853-64807f359604','49c0193b-949e-42fb-a119-cebf448d78b1','4c7eb9d3-4893-4c73-bafa-2c49f44cb838','67cca817-1244-47ee-bcd8-ed7ae61e5098','b484825a-eccf-4924-899d-e76010e52f94','bcbf710f-47cb-4b66-bfd5-80fc02ac4997','b88b616c-1dd1-4fcd-9a9b-4aa266f088d8','cdb4e6d6-2e18-4f08-a710-0cda40fb1097','4837e730-3617-40f7-a7ff-8d5ceaefaee5','c69035a8-a7ef-43ef-bb8b-55752851e1c7','71f065cf-f795-4631-8714-d700266f589a','da26b4c6-177b-40e5-b674-57ce64974b7e','dadcda57-bba8-4e02-bee3-011690115fc3','d6ee3e0e-6a0f-429d-bf78-a32074b5e40d','4537a23a-126f-4882-8667-2b48437c4861','9ac63e88-9820-40f6-bd9c-78067095fe46','277a1219-1ade-4270-a18d-52187005aaaa','4e847ead-d87c-4b36-87a9-17406804b2a9','7ee6e26a-5206-41c0-9b12-a0d28f5774f1','54bd0e8c-9dee-4625-914d-c9905a1551cc','ff1df5e5-2ff7-4c10-a25d-854d9c45e1f9','5b0f35c7-fb98-4adb-922f-09f132832680','b943a3e3-4382-4073-8dc4-8f8597626ef5','54305701-25fb-4b59-8cb7-f0cb17829fec','9f455fe1-15d8-4b98-87e3-d48d10ba60dc','c7f3a362-0d49-4d03-b86f-6ae10b36fa4d','c2d34e4e-e53b-4aae-a6fc-4e19b0df5b52','2555edcc-2a3f-4817-abce-69850a6ee599','0b4a54b1-2cf4-4733-b501-4e5489b2ad96','a6bcfc50-7f33-4066-8b82-20d80382030c','8723494e-1a0f-4760-9ad7-78b3e6ff9290','5239e0c9-9e13-4fd6-981b-d0d14fca7b33','27abaeb0-0654-4dec-bffe-65fd8fe4d183','5d074783-4fcb-4ad9-8980-c827f79148c6','192df08a-0793-48d9-9bc6-3b1086162be7','89d1227a-551a-42c7-97fa-7767b60b4ff6','85de2ffe-4f9f-42b1-a710-3148cf96b27d','1e8e13af-731a-420d-b53a-dae06f99ba87','22a4ef95-69b4-45b8-af96-aef17111d87e','e1272d7d-56d6-4881-a222-398b2bd0ac85','240e9be9-94e2-4c77-8088-8a5dc513e16a','1308240c-8d9f-4c0d-b49c-6ae2d2ac566c','88f4e856-aaca-45f4-b9a4-2fa6da5a9c3b','dcfdfd8e-987f-41ab-8236-954a569614f6','ab531011-5e75-4435-8a79-7b861901c842','c918af6e-9eaa-472d-98e4-ebc07a8df4ac','a891a463-ffb8-4072-bcca-09863642008c','ec6ee845-7f7b-48b3-aca7-616649aca3b1','019782ec-b3b2-4fbd-af43-b181c33af072','48dd2d9f-4248-4b7d-ba56-8f0673847c4a','71b8c0f4-f022-4cee-bffe-7ce25f24df58','329028b7-02be-4a73-a4ad-7b918ce31f8e','ca00231b-44ff-45d9-8612-68b347f1bebb','0df64b47-cb21-413f-82f0-66dea45362e0','03010aab-7214-4bdb-b046-803f6c63bd58','2f49ce00-56f2-4e25-b8ee-bc02c2d3cb75','8411561c-7f06-4113-a47c-9faef2a413ef','81ce0e94-d7e6-433c-8f8f-1d3e6d3bea32','1c5d6930-16f5-4f19-9597-42696a07f4ef','5d66caed-6b29-4dbd-9c2a-17b7bc7f8cd9','ab37a878-c25c-4cc8-898c-bbabeb59099b','e389d8c0-6900-41da-89e5-47a0fd58040b','af07a4d2-9a2c-439c-b2a2-b9a1873c91a1','d5fed0c9-989f-4b8e-9506-f18967923209','90a23a15-98b8-45b4-bb62-fb13ec80c9cd','40ccf770-41d0-4855-9373-6e09f81b3b9f','277b39fb-ff53-4d5b-b9d0-a4c5f9bf65c4','463431c5-049e-4b19-a121-9bf8f0d89cf7','e4a41c59-da25-4b8e-95ab-dec13e480c75','7d16a6b8-9205-4cc8-9e84-88ed91101369','cd54ce46-d4b0-417a-a942-9f5b1ed1e313','42ed89a0-8398-4cc2-bc64-813191a79102','cc4080a0-26eb-4263-95bf-3c35e7e8b21a','0543b905-b410-4041-8793-31e40a5c5015','fb85a9fb-b320-4f44-ad27-27ce25dd7ea6','393fa931-99fe-42f5-8efe-93b47ac252e8','0bb9afea-0f2a-427f-a5b7-cf060f7eb19a','b319565c-a239-4f35-8bb4-ecaf88411c98','680a8dba-79b4-468b-be05-fd2da8c295e3','cb787658-0d94-4bea-91df-f921ac36acfb','e2592dfb-19d7-4079-bf86-9e58823c54be','4b8492d3-f880-4236-9ceb-6af6cfee955a','396741eb-4771-44ce-9818-2faf0dc48785','ab75226b-d1f4-4030-8c00-0db25dab9e66','fcca1a41-d0a2-4fd1-916c-ea93b1715c62','0a7a0e65-4699-4af3-b0b6-b3b7d1f9b61e','a2b9f9ca-efa6-4a0f-87ef-36b983536d7f','09e887de-785e-4492-b5c5-76453e741303','9228f0b3-594d-40aa-a309-ecb4ad91ac8a','643a1c40-da9c-408e-8e7e-acc7b116abef','e9a78007-4c5a-4f4a-9ca7-4ddbea48d5ce','d450505c-d0fe-434c-a65b-e3b6ed137936','4f703292-5654-4233-8207-a5b259286fa1','6e132a2b-ff6e-49ee-936c-c235800a3e8e','600373d6-de16-4659-8b56-71e43046615d','e23fb365-a975-45ab-8f0e-a94f720a1191','884e0dee-1e21-4694-b5e2-4b6874d89bba','caaa669b-09b3-4d48-910b-bbca8aefe34b','f7affa0b-e3a1-4d0f-8611-086f6d5ce533','cea8020b-4b5f-4488-8bc6-b7ed8831eb5a','6d7227d4-780f-4ead-b97c-ddde5c21d9cc','872f6f37-329e-41c7-b460-f470a6040df5','4d437797-b67c-453d-a007-ad50a92e7e61','e41fd9c8-6000-495b-8982-485bc58231af','65c6c3b1-7e18-4d86-8c72-06602ef4802a','1c1461eb-4b6f-4e7d-9357-e4fda235f98d','cd888a6f-e038-45f6-8ab3-962fd2915cad','caad0940-6b15-4a83-a784-75cd4bab2d00','96890af6-1d96-4133-a361-b095a71fe61a','6f6b4281-4693-40b6-b4cd-3903ae049b05','407f63e1-1e14-4634-9a46-2b55078eae2f','dbe85870-ccab-40d6-b8ea-ce2da785bfe3','906e2f96-94de-4ac0-a3a5-480fdd16c706','78661eb6-7323-44e8-b0b1-858987645490','3ae2324c-642b-4c05-8e10-2f99c6fb6101','3069ef97-f4ce-4bda-a3fc-f1fb09b45fb5','bec5dac8-65b9-4a4f-8f05-bbc04b4a693b','8ca548b1-e247-410c-8b35-a8602184fc6e','9ec5e0fe-90a8-4555-b01f-f6746cc7eadc','56bd51ee-2b59-44c1-ac6a-63526c033db4','6d142dae-497c-4a3c-9b2d-b05bb5fa8b75','a02d8dec-16f3-4f27-ad61-10f69dbde02e','d9bcbcb2-c1aa-43ac-aa43-b22d713ebf8d','3c23dd29-5e74-42ca-a143-3834719bbab4','12c6ef6b-9987-4f7a-836a-d8ebc1539499','b1602be4-58eb-47f2-8a15-2873662d3522','bbd50cba-468a-47a3-b958-29f84085c131','9fa7378f-b213-49a2-b545-89a07df0ddc8','fb3ddcaf-d335-4539-812c-48d73b279b9f','905799e4-a006-4008-af4e-e4c98b01b46e','0047ce7a-8467-4e1f-9f9c-a11344a7bb35','4bcf6756-fba5-4d00-ace2-3a68914aaedc','6850bd60-2298-4727-8151-57699662e12f','855b589c-aa90-43b3-9ff7-13d5ce2880e4','b9a4ade7-15d6-4af7-a4f2-a6b91d167f0b','35cb9e8c-32a1-47a8-a1a3-bbfcd0d926b4','74381c11-06e6-4cc9-acec-749cb4e8d825','b258c637-9be9-4c3a-813d-dd6e8ed20717','a92f60b8-1418-4de9-9786-3524ee8ab996','2384a765-4a08-4c55-9f3f-f531b9b67b72','3f2c776f-ad72-4e04-a5a9-7a7be0783da7','316eb798-e858-485d-a72f-9fcacbde5d21','4e3578b3-7f06-4dc5-a108-063a481a5972','9b74f1f0-90a4-4e9f-bd7d-3ac1bc5cd957','a49123ea-33a1-40c1-bfbe-ff9b0342f4b9','7566975a-b6c8-4fa3-983f-b77d6c64e944','82641d8f-2e3e-4603-ae81-32107ca29aac','0bb9b32a-91c5-416c-b8ff-15df930ab718','93c76552-809e-45a7-9183-4cb6f22f1471','b2e67683-7820-4d4e-bb74-8031b019db58','7037e380-4c35-4b64-bebf-216753fe701e','e9de9fa2-0b97-4d11-b6a4-0d041bb687bb','b8b4d4a7-ba34-42bc-a0d0-8dc23f824e55','ebeb3085-76e0-4bfb-837e-4ce507576f49','ceda4f6b-2e67-4a4b-9f33-77bfc22486b5','643e32f8-691b-4fc3-aaba-6514913dc32a','9b837431-1026-49ae-b712-8d63f8655f30','6f285fd5-41b6-4668-9eb4-9aee1c7e3be1','e75c3cf6-7b0e-49ef-aaf4-61818487ca8a','b3068612-101a-436c-bbd4-2a4a7fce03d3','e4f06a09-4ac7-4c96-aa6a-a40fa3320643','e48871d2-78af-4392-a011-a54b7bcbcbfa','c9b52d0c-5576-4175-b33b-e50166650f58','07524c25-fe19-4dfa-8e63-28e9ff2562c5','6ab0b168-35a4-402a-94f6-2b7c6178025e','07890e44-5d09-4827-9b82-b93622488f06','9471cffd-f76d-4814-a85c-4d67ca72752b','277c5a96-9e8c-4e9a-b78f-353513ba5b36','89abae49-6c73-4cbb-b7aa-f097a4e495a2','1fc6250f-ef15-4a46-bc27-6c00a3c1adbe','cdabd0f1-dceb-4456-bb75-666be11006ad','6ac5bde6-b0a4-4266-bd39-f1d79db29bdf','6f92d4be-a1cd-4ade-93f6-1c9642c85186','ddd17835-b103-4e50-9887-9c4736d0ba51','fe2c8c99-2a41-494f-9b26-1450eb58a7f2','c9563e1a-0604-4f43-8ee1-bd899a57fff8','a841625b-6745-4fe0-9ed9-b77061b79426','ee280ef1-774a-4164-9da9-0efc14ed4d5a','36ae3dd3-de19-4d35-93e0-5e219190a386','a2f1a1fc-4aa0-48a0-b00a-e61fae148000','af2e4365-d085-4b40-89e1-c2b4b057b8f6','25e15d0d-78f5-4254-8d49-9a7318404363','ba7155b0-e1f4-4baf-b02c-fa09e974a388','9c3df217-c519-4a25-90d6-d83eda2594d7','61619664-4fe2-4c57-9f70-c8e11e41e919') group by symbol,SUBSTR(to_char(create_time,'YYYY-MM'),1,7) order by A desc")
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

'''
print('sheet6')
##sheet6币币交易明细数据
##bz-usdt
cursor = conn.cursor()
cursor.execute("SELECT * FROM match_result_bz_usdt T  WHERE  direction  in ('0','1') and consign_id is not null and  SUBSTR(to_char(create_time,'YYYY-MM'),1,7)>'"+lastweekdate+"'")
rows = cursor.fetchall()
sheet6 = f.add_sheet(u'币币交易明细',cell_overwrite_ok=True) #创建sheet
sheet6.write(0,0,'')
sheet6.write(0,1,'用户id')
sheet6.write(0,2,'挂单id')
sheet6.write(0,3,'对手方挂单id')
sheet6.write(0,4,'成交价')
sheet6.write(0,5,'数量')
sheet6.write(0,6,'撮合成交时间')
sheet6.write(0,7,'交易对')
sheet6.write(0,8,'方向：0买入、1卖出')
sheet6.write(0,9,'手续费')
sheet6.write(0,10,'是否主动方：0否,1是')
sheet6.write(0,11,'创建时间')
sheet6.write(0,12,'创建人')
sheet6.write(0,13,'更新时间')
sheet6.write(0,14,'更新人')
sheet6.write(0,15,'删除标记:0正常1删除')

for i in range(len(rows)):
         for j in range(len(rows[i])):
              sheet6.write(i+1,j,rows[i][j])

#币币交易明细函数定义
def bidetail(flc):
     global a,i
     a=i
     cursor = conn.cursor()
     cursor.execute("SELECT * FROM "+flc+" T  WHERE  direction in ('0','1')  and consign_id is not null and  SUBSTR(to_char(create_time,'YYYY-MM'),1,7)>'" + lastweekdate+"'")
     rows = cursor.fetchall()
     for i in range(a+2,len(rows)+a+2):
              for j in range(len(rows[i-a-2])):
                   sheet6.write(i+1,j,rows[i-a-2][j])

cursor.execute("SELECT tablename FROM pg_tables WHERE tablename NOT LIKE 'pg%' AND tablename like 'match_result%' ORDER BY tablename")
talbles = cursor.fetchall()
for q in range(len(talbles)):  #在此加新的币种交易对
   bidetail(talbles[q][0])

cursor.close()
'''

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
cursor.execute("select num 成交人数,已成交数量,已成交金额,日期,杠杆倍率,b.name 合约 from (select count(distinct a.account_id) num,sum(a.done_number)/2 已成交数量,sum(a.done_number*a.done_average_price)/200 已成交金额,SUBSTR(to_char(updatetime,'YYYY-MM'),1,7) 日期,a.lever 杠杆倍率,a.type_id 合约类型 from contract_consignation a,contract_account b where a.account_id=b.id   and b.uid not in ('4e3ef361-a918-4ab7-8e80-9192994efdd3','3d762c98-cc54-4d5c-b55d-a17119b768d4')   and done_average_price is not null    group by SUBSTR(to_char(updatetime,'YYYY-MM'),1,7),a.lever,a.type_id order by SUBSTR(to_char(updatetime,'YYYY-MM'),1,7)  desc    ) a,contract_type b      where a.合约类型=b.id")
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

#sheet9eos
conn = psycopg2.connect(database="eos", user="qaread",password="swerbn!gsWQg23", host="47.75.75.33", port="25433")
#抵押bz
sheet9 = f.add_sheet(u'eos',cell_overwrite_ok=True) #创建sheet
sheet9.write(0,0,'日期')
sheet9.write(0,1,'抵押bz人数')
sheet9.write(0,2,'抵押bz数')
cursor = conn.cursor()
cursor.execute("select to_char(create_time, 'YYYY-MM') date,count(  DISTINCT user_id) 人数,sum(lock_bz) bz数 from  eos_lock_detail  where    user_id not in('2285c3cb-3512-4732-97e6-cc3614623872', '8e6df824-b345-44e0-8a80-b95294e9f3b3','e203b30b-0d54-4ffa-8ba2-d344f454b5cd','e68a6cd2-d712-4110-a211-4ca68726687d', 'ccdf5775-624a-4740-bb7a-5c8987d05968', 'ed4bd8c3-81cf-4664-bf1d-26022b577e26', '4e3ef361-a918-4ab7-8e80-9192994efdd3', '3d762c98-cc54-4d5c-b55d-a17119b768d4') group by to_char(create_time, 'YYYY-MM')  order by date desc")
rows = cursor.fetchall()
for i in range(len(rows)):
         for j in range(len(rows[i])):
              sheet9.write(i+1,j,rows[i][j])

#赎回bz
a=i
sheet9.write(a+3,0,'日期')
sheet9.write(a+3,1,'赎回bz人数')
sheet9.write(a+3,2,'赎回bz数')

cursor.execute("select to_char(create_time, 'YYYY-MM') date,count(  DISTINCT user_id) 人数,sum(unlock_bz) bz数 from  eos_unlock_detail  where    user_id not in('2285c3cb-3512-4732-97e6-cc3614623872', '8e6df824-b345-44e0-8a80-b95294e9f3b3', 'e203b30b-0d54-4ffa-8ba2-d344f454b5cd', 'e68a6cd2-d712-4110-a211-4ca68726687d', 'ccdf5775-624a-4740-bb7a-5c8987d05968', 'ed4bd8c3-81cf-4664-bf1d-26022b577e26', '4e3ef361-a918-4ab7-8e80-9192994efdd3', '3d762c98-cc54-4d5c-b55d-a17119b768d4') group by to_char(create_time, 'YYYY-MM')  order by date desc")
rows = cursor.fetchall()
for i in range(a+3,len(rows)+a+3):
         for j in range(len(rows[i-a-3])):
              sheet9.write(i+1,j,rows[i-a-3][j])


#市场抵押bz总量

a=i
sheet9.write(a+3,0,str(date)+'市场抵押bz总量')

cursor.execute("select (select sum(lock_bz) from  eos_lock_detail  where to_char(create_time, 'YYYY-MM')<=' " +str(date)+ " ')-(select sum(unlock_bz) from  eos_unlock_detail  where to_char(create_time, 'YYYY-MM')<=' " + str(date) + " ')")
rows = cursor.fetchall()
for i in range(a+3,len(rows)+a+3):
         for j in range(len(rows[i-a-3])):
              sheet9.write(i+1,j,rows[i-a-3][j])

#已分配cpu	
		  		  
a=i
sheet9.write(a+3,0,str(date)+'前已分配cpu资源总量')

cursor.execute("select nonfee_count from eos_period_cfg    where to_char(effect_time, 'YYYY-MM')<='" +str(date)+ "'  order BY effect_time limit 1")
rows = cursor.fetchall()
for i in range(a+3,len(rows)+a+3):
         for j in range(len(rows[i-a-3])):
              sheet9.write(i+1,j,rows[i-a-3][j])
			  

#难度			  		  
a=i
sheet9.write(a+3,0,'日期')
sheet9.write(a+3,1,'difficulty')

cursor.execute("select  distinct to_char(create_time, 'YYYY-MM') date,difficulty from eos_nonfee_info    where to_char(create_time, 'YYYY-MM HH24:mi:ss') like '%00:00:00' order by date desc")
rows = cursor.fetchall()
for i in range(a+3,len(rows)+a+3):
         for j in range(len(rows[i-a-3])):
              sheet9.write(i+1,j,rows[i-a-3][j])

#当前CPU使用量
a=i
sheet9.write(a+3,0,'日期')
sheet9.write(a+3,1,'每日CPU使用量')

cursor.execute("select to_char(create_time, 'YYYY-MM') date,count(*) from  eos_resource_detail  where    user_id not in('2285c3cb-3512-4732-97e6-cc3614623872', '8e6df824-b345-44e0-8a80-b95294e9f3b3', 'e203b30b-0d54-4ffa-8ba2-d344f454b5cd', 'e68a6cd2-d712-4110-a211-4ca68726687d', 'ccdf5775-624a-4740-bb7a-5c8987d05968', 'ed4bd8c3-81cf-4664-bf1d-26022b577e26', '4e3ef361-a918-4ab7-8e80-9192994efdd3', '3d762c98-cc54-4d5c-b55d-a17119b768d4') group by to_char(create_time, 'YYYY-MM') order by date desc")
rows = cursor.fetchall()
for i in range(a+3,len(rows)+a+3):
         for j in range(len(rows[i-a-3])):
              sheet9.write(i+1,j,rows[i-a-3][j])		  

#当前CPU使用总量
a=i
sheet9.write(a+3,0,'日期')
sheet9.write(a+3,1,'每日CPU使用量（未剔除量化）')
cursor.execute("select to_char(create_time, 'YYYY-MM') date,count(*)from  eos_resource_detail  group by to_char(create_time, 'YYYY-MM') order by date desc")
rows = cursor.fetchall()
for i in range(a+3,len(rows)+a+3):
         for j in range(len(rows[i-a-3])):
              sheet9.write(i+1,j,rows[i-a-3][j])  
cursor.close()

print(date)
f.save('E:\\gj\\everydayjob\\'+str(date)+'.xls')#保存文件









print('郑商所行情开始')


#定义getdate函数，获取系统当前日期，并将日期'2018-08-02'转换成'20180802'
def getdate(num):
    date=datetime.datetime.now().date() #获取系统当前日期
    srdate=date-datetime.timedelta(hours = 24*num) #srdate为系统日期减num为单位的日期
    srdate=str(srdate).replace('-','') #替换-为空
    return srdate  #返回srdate


def srdata(date):
  try:
     request.urlretrieve('http://www.czce.com.cn/cn/DFSStaticFiles/Future/'+date[0:4]+'/'+date+'/FutureDataDaily.xls','E:\\code\\ffe.xlsx')
     df=pd.read_excel('E:\\code\\ffe.xlsx')
     date=re.search('\d\d\d\d-\d\d-\d\d',df.columns.values[0]).group()
     date=date.replace('-','/')
     df.columns=df.ix[0] #将第一行设为行名
     df=df.drop([0]) #删除第一行
     nan=df.isnull()[df.isnull().今结算==True].index.tolist()  
     df=df.drop(nan) 
     df=df.rename(columns={'交割结算价':'日期'})
     df['日期']=date
     odf=pd.read_excel('E:\\code\\zssfuture.xlsx')  
     pd.concat([odf,df]).to_excel('E:\\code\\zssfuture.xlsx')
     print('文件保存成功')
  except:
     print('error')
     return 1

i=1
date=getdate(i)
b=srdata(date)

o=7
while (b==1 and o>0):
  i=i+1
  o=o-1
  date=getdate(i)
  b=srdata(date)
print('郑商所行情结束,日期',date)



