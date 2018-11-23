import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
df=pd.read_excel('E:\\code\\srdata.xlsx')         #读取excel文件
df=df.drop_duplicates().sort_values(by='date')    #去重并根据日期升序排列
nan=df[np.isnan(df.settle)==True].index.tolist()  #确认空值序列（index）
df=df.drop(nan)    
df.index=df.date # df序列设置为日期