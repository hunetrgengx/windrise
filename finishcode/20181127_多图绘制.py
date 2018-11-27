import requests
import re
from bs4 import BeautifulSoup
import time
import os
import pandas as pd
import usuallytool as ut #导入自建函数usuallytool
import datetime as dt
import numpy as np
import random as re
import matplotlib.pyplot as plt
import mpl_finance as mpf
from datetime import datetime
import matplotlib.gridspec as gridspec


dfc=ut.dailykl('SR1409')
dfb=ut.dailykl('SR1405')
dfa=ut.dailykl('SR1401')

dfcc=dfc[(dfc[0]>'2013-10-01') & (dfc[0]<'2014-03-01')]
dfbb=dfb[(dfb[0]>'2013-10-01') & (dfb[0]<'2014-03-01')]
dfaa=dfa[(dfa[0]>'2013-10-01') & (dfa[0]<'2014-03-01')]

xdfa=ut.transcandledata(dfaa)
xdfb=ut.transcandledata(dfbb)
xdfc=ut.transcandledata(dfcc)    

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

mpf.candlestick_ohlc(ax1, xdfa, width=0.5, colorup='r', colordown='g')
mpf.candlestick_ohlc(ax2, xdfb, width=0.5, colorup='r', colordown='g')
mpf.candlestick_ohlc(ax3, xdfc, width=0.5, colorup='r', colordown='g')
ax4.plot(xdf,color='b',style='-o')


ax1.set_title('1901',fontsize=12,color='k')
ax2.set_title('1905',fontsize=12,color='k')
ax3.set_title('1909',fontsize=12,color='k')
#分图如何把他分进去
ax4.set_title('09/05价差',fontsize=12,color='k')
plt.show()    


xdf=[]
for i in range(len(dfcc)):
    mix=[xdfc[i][4]-xdfb[i][4]]
    xdf.append(mix)  
    
    
    

