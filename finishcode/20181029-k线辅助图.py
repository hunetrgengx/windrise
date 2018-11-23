import psycopg2,datetime,re
from urllib import request
import pandas as pd
import datetime as dt
from decimal import *
import numpy as np
import random as re
import matplotlib.pyplot as plt
import mpl_finance as mpf
from datetime import datetime
import matplotlib.gridspec as gridspec
import tushare as ts
import matplotlib.pyplot as plt

# 支持中文
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
print('开始读取数据库..')
#提取数据
conn = psycopg2.connect(database="t2tservice", user="qaread",password="swerbn!gsWQg23", host="52.69.40.154", port="25430")
cursor = conn.cursor()
cursor.execute("select distinct price,to_char(create_time,'yyyy-mm-dd hh24:mi:ss') from match_result_bz_usdt where symbol='bz-usdt'  and  create_time>='2018-10-26' order by to_char(create_time,'yyyy-mm-dd hh24:mi:ss') desc")
middata = pd.DataFrame(data=cursor.fetchall())
middata=middata.rename(columns={0:'price',1:'date'})
print('数据库读取完毕!')


data = ts.get_k_data('603026', ktype='D', autype='qfq', start='2017-01-17', end='')
prices = data[['open', 'high', 'low', 'close']]
dates = data['date']
candleData = np.column_stack([list(range(len(dates))), prices])

#数据分组
a=datetime.now()
#生成日期序列
index=[]
for i in range(200):
    index.append(str(a-dt.timedelta(minutes=1*i))[:19])


print('原图开始绘制')
original=[]
unit=[]
high=middata.price[0]
low=middata.price[0]
close=middata.price[0]
open=middata.price[0]
for i in range(198):
     a=middata[(middata.date>=index[i+1]) & (middata.date<index[i])]
     if a.index.min()>=0: 
      open=a.price[a.index.min()]
      high=a.price.max()
      low=a.price.min()
      close=a.price[a.index.max()]
      unit=[i,open,high,low,close]
     elif  np.isnan(a.index.min()):
      unit=[i,close,close,close,close]
     original.append(unit)

print('随机倍数图形开始绘制')
randomp=[]
unit=[]
high=middata.price[0]
low=middata.price[0]
close=middata.price[0]
open=middata.price[0]
for i in range(198):
     a=middata[(middata.date>=index[i+1]) & (middata.date<index[i])]
     if a.index.min()>=0: 
      open=a.price[a.index.min()]+Decimal.from_float(re.random()-0.5)*Decimal.from_float(0.002)*(high-low)/high
      high=a.price.max()+Decimal.from_float(re.random())*Decimal.from_float(0.0015)*(high-low)/high
      low=a.price.min()-Decimal.from_float(re.random())*Decimal.from_float(0.0015)*(high-low)/high
      close=a.price[a.index.max()]+Decimal.from_float(re.random()-0.5)*Decimal.from_float(0.002)*(high-low)/high
      unit=[i,open,high,low,close]
     elif  np.isnan(a.index.min()):
      unit=[i,close,close,close,close]
     randomp.append(unit)




'''
data = ts.get_k_data('600519', ktype='D', autype='qfq', start='2017-09-17', end='')
prices = data[['open', 'high', 'low', 'close']]
dates = data['date']
candleData = np.column_stack([list(range(len(dates))), prices])

fig = plt.figure(figsize=(10, 6))
ax = fig.add_axes([0.1, 0.3, 0.8, 0.6])
mpf.candlestick_ohlc(ax, mid[:100], width=0.5, colorup='r', colordown='g')
plt.show() 


需要解决的问题：1、空值问题；2、如何让价格波动起来
'''
print('复合图形开始绘制')
mixp=[]
unit=[]
high=middata.price[0]
low=middata.price[0]
close=middata.price[0]
open=middata.price[0]
base=middata.price[0]/Decimal.from_float(prices.close.values[0])
for i in range(198):
    a=middata[(middata.date>=index[i+1]) & (middata.date<index[i])]
    if a.index.min()>=0: 
        open=a.price[a.index.min()]*Decimal.from_float((prices.open.values[i+1]/prices.open.values[i]))
        high=a.price.max()*Decimal.from_float((prices.high.values[i+1]/prices.high.values[i]))
        low=a.price.min()*Decimal.from_float((prices.low.values[i+1]/prices.low.values[i]))
        close=a.price[a.index.max()]*Decimal.from_float((prices.close.values[i+1]/prices.close.values[i]))
        base=a.price[a.index.min()]/Decimal.from_float(prices.open.values[i])
    elif  np.isnan(a.index.min()):
        open=base*Decimal.from_float(prices.open.values[i])
        high=base*Decimal.from_float(prices.high.values[i])
        low=base*Decimal.from_float(prices.low.values[i])
        close=base*Decimal.from_float(prices.close.values[i])
    if (a.price[a.index.min()]-a.price[a.index.max()])*(open-close)>=0:
        unit=[i,open,max(high,low),min(high,low),close]
    elif (a.price[a.index.min()]-a.price[a.index.max()])*(open-close)<0:
        unit=[i,close,max(high,low),min(high,low),open]
    mixp.append(unit)        

                

# 定义figure
plt.figure()

# 分隔figure为2行2列
gs = gridspec.GridSpec(2,2)
# 将ax1定义在行列1
ax1 = plt.subplot(gs[0, 0])
# 将ax2定义在行1列2
ax2 = plt.subplot(gs[0, 1])
ax3 = plt.subplot(gs[1, 0])
ax4 = plt.subplot(gs[1, 1])

mpf.candlestick_ohlc(ax1, original[:100], width=0.5, colorup='r', colordown='g')
mpf.candlestick_ohlc(ax2, randomp[:100], width=0.5, colorup='r', colordown='g')
mpf.candlestick_ohlc(ax3, mixp[:100], width=0.5, colorup='r', colordown='g')
mpf.candlestick_ohlc(ax4, candleData[:100], width=0.5, colorup='r', colordown='g')
ax1.set_title('原图',fontsize=12,color='k')
ax2.set_title('随机倍数扩大',fontsize=12,color='k')
ax3.set_title('复合股票K线',fontsize=12,color='k')
ax4.set_title('股票K线',fontsize=12,color='k')

plt.show()
