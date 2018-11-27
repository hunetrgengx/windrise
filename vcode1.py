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

# 支持中文
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

df09=ut.dailykl('SR1409')
df05=ut.dailykl('SR1405')
df01=ut.dailykl('SR1401')
