# -- coding: UTF-8 --
import random as ra
import pandas as pd
import usuallytool as ut 
import talib 
import numpy as np 
import matplotlib as mpl
import re

f=open(r'E:\gj\测试\白糖_2009-06-19_19日下午主产区现货报价综述.txt',encoding='utf-8')
a=f.read()
getre = re.match(r'(\d\d)日.*?(\d\d\d\d-\d\d-\d\d).*?柳州(.*?)(\d.*?)元',a,re.S)
getre.group(0)
getre.group(1)
