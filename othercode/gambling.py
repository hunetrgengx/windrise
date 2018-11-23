#最简化，不实例化，完全竞争市场，不考虑对方策略
import random as ra
import pandas as pd




def gambling():
   poker=12
   star=3
   count=0
   
   while poker>=0:
      if (poker>0 and star>0):
          compition=ra.randint(0,1) #可以考虑不比
          compition=1
          if compition==1:
              play=ra.randint(-1,1)
              poker=poker-1
              star+=play 
              count+=1
          elif compition==0:
              count+=1

      elif (poker>=0 and star==0):
          result='lose'
          break
          
      elif (poker==0 and star>=3):
          result='win'
   
          break
      elif (poker==0 and (star in (1,2))):
          result='lose'
          break
   
   return count,result,poker,star

df=pd.DataFrame()
for i in range(10000):
 a=list(gambling())  #tuple转换成list
 df[i]=a

data=pd.DataFrame(columns=['count','poker','star','result'])
data['count']=df[df.index==0].values.tolist()[0]
data['result']=df[df.index==1].values.tolist()[0]
data['poker']=df[df.index==2].values.tolist()[0]
data['star']=df[df.index==3].values.tolist()[0]


win=data[data['result']=='win']
wincount=win[u'star'].value_counts() 

print(wincount)


#data.to_excel('gambling.xlsx')