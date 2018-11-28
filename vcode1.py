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
import talib
# 支持中文
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

df=ut.dailykl('SR1409')
close=df[4]
nclose=np.array(close,dtype='f8') #非得做这一步转换，日了狗了
ma5=talib.MA(nclose,5)
