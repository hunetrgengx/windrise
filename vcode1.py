# -- coding: UTF-8 --
import random as ra
import pandas as pd
import usuallytool as ut 
import talib 
import numpy as np 
import matplotlib as mpl
#定义期货投资者Futures investors

class fopen():
    def __init__(self):
            self.price=0
            self.direction=0
            self.date=0
            self.number=0
            self.status=0
            self.profit=0
            self.closing=0


df=ut.dailykl('SR0')
close=df[4]
nclose=np.array(close,dtype='f8') #非得做这一步转换，日了狗了
upper, middle, lower = talib.BBANDS(nclose, matype=talib.MA_Type.T3)
lower.tolist()
df['lower']=lower

position=[]
over=[]
mid=[]
num=0
for i in range(25,len(df[4])):
    #判断买入价及是否买入
    if df[4][i]<df['lower'][i]:
        a=fopen()
        a.price=df[4][i]
        a.direction=1
        a.number=i
        a.date=df[0][i]
        a.status=1
        position.append(a)
    #判断卖出的问题
    if len(position)==0:
            c=1
    elif len(position)>0:
        for j in range(len(position)):
            if df[4][i]>position[j].price*1.02:
                position[j].status=0
                position[j].closing=position[j].price*1.02
                position[j].profit=position[j].price*0.02*10
            elif df[4][i]<position[j].price*0.98:
                position[j].status=0
                position[j].closing=position[j].price*0.98
                position[j].profit=-position[j].price*0.02*10


over=[] 
win=[]
lose=[]
winprofit=0
loseprofit=0
for i in range(len(position)):          
    if position[i].status==0:
        over.append(position[i])

for i in range(len(position)):
    if position[i].profit>0:
        win.append(position[i])
        winprofit+=position[i].profit
    elif position[i].profit<0:
        lose.append(position[i])
        loseprofit+=position[i].profit

result=[]
for i in range(len(position)):
        result.append([position[i].price,position[i].closing])
result=pd.DataFrame(data=result)
result.to_excel('a.xls')
#策略：交易者根据收盘进行决定是否开仓，如果收盘价高于10日均线，则进行建仓，这个仓位盈利百分之10、亏损百分之5平仓

nlower=[]
for i in range(len(lower)):
        nlower.append(lower[i].item()



nnclose=[]
for i in range(len(df[4])):
        nnclose.append(float(df[4][i]))