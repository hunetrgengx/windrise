import psycopg2,datetime,re
from urllib import request
import pandas as pd
import random as rd 
import matplotlib.pyplot as plt

sum=100


def kaili(n,position,win):
    sum=50000
    for i in range(n):
      d=rd.random()
      
      if d>=0.6:
           sum=sum+position*sum*(-0.1)
           
      elif d<0.6:
           sum=sum+position*sum*0.1
           
    return round(sum,2)
    
kaili(10,0.1,0.6)
a=[]
for i in range(400):
    a.append(kaili(200,0.1,0.6))

df=pd.DataFrame(columns={'result'},data=a)

lose=df[df.result<100]