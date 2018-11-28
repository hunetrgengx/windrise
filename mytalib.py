# -- coding: UTF-8 --
#talib用法
import talib
import numpy as np 
import usuallytool as ut #导入自建函数usuallytool
import matplotlib.pyplot as plt



# 支持中文
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

df=ut.dailykl('SR1409')
close=df[4]
nclose=np.array(close,dtype='f8') #非得做这一步转换，日了狗了
ma5=talib.MA(nclose,5)
'''
from talib import MA_Type #终于懂了
upper, middle, lower = talib.BBANDS(close, matype=MA_Type.T3)
upper, middle, lower = talib.BBANDS(close, matype=talib.MA_Type.T3)
'''