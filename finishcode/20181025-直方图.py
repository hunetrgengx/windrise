import psycopg2,datetime,re
from urllib import request
import pandas as pd
import random as rd 
import matplotlib.pyplot as plt



def kaili(n,position,win):
    sum=50000
    for i in range(n):
      d=rd.random()
      
      if d>=0.5:
           sum=sum+position*sum*(-0.3)-12
           
      elif d<0.5:
           sum=sum+position*sum*0.5-12
           `
           
           
           
           
           
           
           
           
           
           
           
           
           
           
           
           
           
           
           
           
           
           
           
           `
    return round(sum,2)
    
kaili(10,0.1,0.6)
a=[]
for i in range(1000):
    a.append(kaili(200,1/30,0.5))

df=pd.DataFrame(columns={'result'},data=a)

lose=df[df.result<50000]

df.result.hist(bins=30)
plt.show()
d=df['result'].hist(bins=30).get_figure()
d.savefig('2.jpg')