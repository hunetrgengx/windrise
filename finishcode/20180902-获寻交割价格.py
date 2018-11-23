import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
df=pd.read_excel('E:\\code\\zssfuture.xlsx')         #读取excel文件
df=df.drop_duplicates(['日期','品种月份']).sort_values(by=['日期','品种月份'])   #利用日期和品种月份进行去重并根据日期升序排列
nan=df.isnull()[df.isnull().今结算==True].index.tolist()    #确认空值序列（index）
df=df.drop(nan)                                   #去除空值列
df=df[df.品种月份.str.contains(r'SR.*')] #取出白糖数据
df.index=np.arange(1,df.shape[0]+1,1)    #重新设置索引，arrange初始值，终值，步长，记得终值并不会取到，也就是说最后一个数是终值-步长
df=df.rename(columns={'品种月份':'contract','今结算':'settle','日期':'date'}) #替换columns
for i in (df.columns.drop('contract').drop('date')):   #in 里面的东西可以用逗号隔开，则为这个东西
   df[i]=df[i].apply(lambda x:float(str(x).replace(',','')))  #替换所有列，将，去除

#将df数据展示成以品种月份为行名的数组
df.index=df.date
df.contract.drop_duplicates().values.tolist()
ndf=pd.DataFrame(index=df.index.drop_duplicates(),columns=df.contract.drop_duplicates().sort_values().values.tolist())
a=df.contract.drop_duplicates().sort_values().values.tolist()
for i in range(len(a)):
  ndf[a[i]]=df.settle[df.contract==a[i]]


lastdf=pd.DataFrame(columns={'contract','price'})
for i in (ndf.columns):
	aa=ndf[i]
	b=aa.drop(aa.isnull()[aa.isnull()==True].index.tolist())[-1:]  #这个[-1:]额切片很精髓
	e=pd.DataFrame(index=b.index,columns={'contract','price'})
	e.contract=aa.name
	e.price=b.values
	lastdf=lastdf.append(e)   #添加行用append，不要利用index进行匹配

lastdf=lastdf.drop_duplicates(['price']).sort_values(by=['contract'])  
lastdf.to_excel('交割价.xls')