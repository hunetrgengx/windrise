# -- coding: UTF-8 --
import random as ra
import pandas as pd
import usuallytool as ut 
import talib 
import numpy as np 

#定义期货投资者Futures investors
class fior():
    def __init__(self,name):
        self.name=name
        self.balance=200000
        self.position=0
        self.time=10
        self.direction=0
        self.price=0
        self.win=0
        self.lose=0

#策略：交易者根据收盘进行决定是否开仓，如果收盘价高于boll线上线，则进行建仓，这个仓位盈利百分之10、亏损百分之5平仓
ming=fior('ming')
df=ut.dailykl('SR0')
close=df[4]
nclose=np.array(close,dtype='f8') #非得做这一步转换，日了狗了
upper, middle, lower = talib.BBANDS(nclose, matype=talib.MA_Type.T3)



print(len(upper))
for j in range(150):     
    for i in range(ming.time+1,len(upper)):
        if upper[i]<nclose[i]:
            ming.position+=1
            ming.balance-=nclose[i]
            ming.time=i
            break    
    
    for i in range(ming.time,len(upper)):
        compareprice=nclose[i]
        lose=nclose[ming.time]*1.1
        win=nclose[ming.time]*0.8
        if nclose[i]>lose:
            ming.balance+=(nclose[ming.time]-(nclose[i])*10+nclose[ming.time])
            ming.lose+=1
            break
        elif nclose[i]<win:
            ming.balance+=((nclose[ming.time]-nclose[i])*10+nclose[ming.time])
            ming.win+=1
            break    
    print(j,ming.balance,i,'平仓价',nclose[i],'开仓价',nclose[ming.time],ming.win,ming.lose)