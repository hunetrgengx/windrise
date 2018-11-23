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

#按照index进行统一合并
sheet2=pd.concat([sheet,rows],axis=1,join='outer')
#统计数据
totaltv=df['TV'].groupby(df['date']).mean()
totalvolume=df['volume'].groupby(df['date']).mean()
index=totaltv/totalvolume*1000  #取指数
ndf=df[(df['date']>'2013/06/01') & (df['date']<'2014/02/01')]    #取日期                    ndf为所需要日期
data=ndf.drop_duplicates(subset='date').sort_values(by='date')   #取不重复日期为序列index   data为index序列
ndata=pd.DataFrame(index=data.index,columns=['SR307','SR309','SR311','SR401','SR403','SR405','SR407','SR409','SR411','SR501','SR503','SR505','SR507','SR509','SR511','SR601','SR603','SR605'])  #设置空的dataframe
ndata.SR307=ndf[ndf['contract']=='SR307'].settle  #利用索引赋值，系统会自动匹配索引，很方便
df.settle.value_counts().head() #统计settle中出现次数最多的价格
df.品种月份.nunique() #品种月份distinct后count





#添加列
data=data.append(a)

#提取数据
df['今结算']   #依据列名提取
df.今结算    #依据列名提取
df.ix[0]  #根据行数筛选
df.ix['line1']  #根据行名称筛选
df.ix[0:2]  #根据行数切片
df.ix['line1':'line2'] #根据行名称切片
df.ix[['line1','line2']] #根据行名称选择多行
df.ix[0:2,['col1','col2']]  #根据行列名称切片

#条件查询
df[df['col1'] == 3]   #根据条件筛选
df[(df['col1'] ==3) &(df['col2'] == 4)] #多条件and查询
df[(df['col1'] ==3) |(df['col2'] == 4)] #多条件or查询

#进行列替换
df[df['日期']==20180625].apply(lambda row: row.今结算.replace(',',''),axis=1)
df['日期'].apply(lambda row: row.今结算.replace(',',''),axis=1)
df[df['日期']==20180625].apply(lambda row: row.今结算.replace(',',''),axis=1)

for i in range(len(df['今结算'])):
    df['今结算'][i]=df['今结算'][i].replace(',','')


#条件查询，且：“&”；或：“|”
newdf=df[(df['date']>'2013/03/12') & (df['date']<'2013/12/12')]

#设置索引，排序，取数组
newdfsr305=newdf[newdf['contract']=='SR305']
newdfsr307=newdf[newdf['contract']=='SR307']
newdfsr305=newdfsr305.sort_values(by='date')
newdfsr307=newdfsr307.sort_values(by='date')

df2013=df[(df['date']>'2013/06/01') & (df['date']<'2014/06/01')]


#groupby后取settle最大值
dff=df2013[['settle','date']].groupby(df['contract']).max()#语句同时会取settle和date的最大值
dff=df2013['settle'].groupby(df['contract']).max()
ddd=df2013[df2013['settle']==dff['settle']]
dd=df2013[['contract','settle','date']].sort_values(by='settle').groupby(df['contract']).head(1)
dd=df2013[['contract','settle','date']].sort_values(by='settle',ascending=False).groupby(df['contract']).head(1)
dd=df2013[['contract','settle','date','volume']].sort_values(['contract','settle'],ascending=[True,False]).groupby(df['contract']).head(1)##这个语句是对的    

df.loc[行标签,列标签]
df.loc['a':'b']#选取ab两行数据
df.loc[:,'one']#选取one列的数据


totaltv=df['TV'].groupby(df['date']).mean()
totalvolume=df['volume'].groupby(df['date']).mean()
index=totaltv/totalvolume*1000
ndf=df[(df['date']>'2013/06/01') & (df['date']<'2014/11/01')]


#利用日期排序后distinct
data=ndf.drop_duplicates(subset='date').sort_values(by='date')

#设置某一列为index
data.index=data['date'].tolist()

#设置空的dataframe
ndata=pd.DataFrame(index=data.index,columns=['SR307','SR309','SR311','SR401','SR403','SR405','SR407','SR409','SR411','SR501','SR503','SR505'])
#新列条件赋值
ndata.SR307=data[data['contract']=='SR307'].settle
#查看是否有重复项，是为true
II.duplicated()

#查询为空的数据
nan=df[np.isnan(df.settle)==True]
df=df[df.今结算.notnull()] #筛选出今结算非空的数组

#修改行列名
data.rename(index={'A':'D', 'B':'E', 'C':'F'}, columns={'a':'d', 'b':'e', 'c':'f'}, inplace = True)

#dataframe 导出为excel
ndata.to_excel('ndata.xls')

#添加列
ndata=pd.DataFrame(columns=[2],data=b)
df=pd.DataFrame(columns={'date','num'},data=rows)  #直接赋值,rows为list
ndata[i]=b   #在原有基础上添加



#行列转置
data=pd.DataFrame(columns=['count','result']) 
data['count']=df[df.index==0].values.tolist()[0]
data['result']=df[df.index==1].values.tolist()[0]


#统计数据
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
df=pd.read_excel('E:\\code\\gambling.xlsx')   
win=df[df['result']=='win']
wincount=win[u'star'].value_counts()  #与wincount=win['star'].value_counts()意义相同，u的意思应该是加个限定条件，具体未知


#!正则匹配
df[df.品种月份.str.contains(r'SR.*')]


#添加交割价格，使用了行列添加的方法
lastdf=pd.DataFrame(columns={'contract','price'})
for i in (ndf.columns):
	aa=ndf[i]
	b=aa.drop(aa.isnull()[aa.isnull()==True].index.tolist())[-1:]
	e=pd.DataFrame(index=b.index,columns={'contract','price'})
	e.contract=aa.name
	e.price=b.values
	lastdf=lastdf.append(e)
