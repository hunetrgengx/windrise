# -- coding: UTF-8 --
#画图
import talib
import numpy as np 
import usuallytool as ut #导入自建函数usuallytool
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np
# 支持中文
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

#导入数据
name='SR1601'
df=ut.dailykl(name)
nclose=df[4]
b=df[0]
close=np.array(nclose,dtype='f8').tolist() #将数据转化成float格式
#开始画图

fig=plt.figure()

plt.title(name)
plt.plot(b,close)
plt.show()

