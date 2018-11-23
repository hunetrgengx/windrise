

import random as ra
import pandas as pd


class gambler():
    def __init__(self,name):
        self.poker = ['a','a','a','a','b','b','b','b','c','c','c','c'] 
        self.star = 3  # 星数
        self.count = 0  # 进行局数
        self.go=ra.randint(0,1) #意愿，在0,1之间徘徊，百分之50几率行动
        self.name=name

#游戏初始化

john=gambler('john')
matchpeople=[john]
countnum=0
outer=[]
winer=[]
names=locals()#用于随机生成名字
for i in range(119):
        names['gambler'+str(i)]=gambler('gambler'+str(i))#循环生成变量，names[]整体为变量
        matchpeople.append(names['gambler'+str(i)])#将对象加入matchpeople中，加入后，因为是引用变量，所以对于其进行操作，单独都会变化


#定义match函数，用于将比赛的两个人员筛选出来,#确定参赛者
def matchg(b):
        c=b[:]   #等于b的切片，这样c变更时，不影响原来的数据
        d=ra.choice(c)  #defence 防御者
        c.remove(d)                       
        a=ra.choice(c)  #attack 攻击者
        match=[a,d]
        return match

#开始比赛
def compition(oo):
     match=matchg(oo)
     acard=ra.choice(match[0].poker)  #0选出acard
     dcard=ra.choice(match[1].poker)  #1选出bcard进行比赛
     match[0].poker.remove(acard)     #0中，将acard去除
     match[1].poker.remove(dcard)   #1中，将bcard去除
     #判断，剪刀石头布
     if ((acard=='a' and dcard=='a') or (acard=='b' and dcard=='b') or (acard=='c' and dcard=='c')):
         match[0].count+=1
         match[1].count+=1
         
     elif ((acard=='a' and dcard=='b') or (acard=='b' and dcard=='c') or (acard=='c' and dcard=='a')):
         match[0].count+=1
         match[1].count+=1
         match[0].star+=1
         match[1].star-=1
         
     elif ((acard=='a' and dcard=='c') or (acard=='b' and dcard=='a') or (acard=='c' and dcard=='b')):    
         match[0].count+=1
         match[1].count+=1
         match[0].star-=1
         match[1].star+=1
         #print(match[0].name,'输给了',match[1].name)
     #print(acard,match[1].name,match[1].count,match[1].star)
     #print(dcard,match[0].name,match[0].count,match[0].star)
     return oo

#定义函数，输入matchpeople，输出outer，winer，新的matchpeople，每局统计数据countlist,主角信息
def out(a):
    global outer,winer,countnum
    A=0
    B=0
    C=0
    #print('a的长度',len(a))
    lena=len(a)
    for i in range(len(a)):
        lenb=len(a)
        if lena>len(a):
            i-=(lena-len(a))
        #print('i=',i,a[i].count,a[i].star,a[i].poker,a[i].name)
        if (a[i].count>0 and a[i].count<12) :
            if a[i].star==0:
                outer.append(a[i])
                a.remove(a[i])
            elif a[i].star>0:
                for j in range(len(a[i].poker)):
                    if a[i].poker[j]=='a':
                        A+=1
                        
                    elif a[i].poker[j]=='b':
                        B+=1
                        
                    elif a[i].poker[j]=='c':
                        C+=1
                        
        elif a[i].count==12:
            if a[i].star<3:
                outer.append(a[i])
                a.remove(a[i])
            elif a[i].star>=3:
                winer.append(a[i])
                a.remove(a[i])

        elif a[i].count==0:
              for j in range(len(a[i].poker)):
                    if a[i].poker[j]=='a':
                        A+=1
                        
                    elif a[i].poker[j]=='b':
                        B+=1
                        
                    elif a[i].poker[j]=='c':
                        C+=1
    countlist=['A:'+str(A),'B:'+str(B),'C:'+str(C)]
    countnum+=1
    countname=countnum
    return countlist,countname,winer,outer,a


df=pd.DataFrame()
qq=[]
for j in range(1000):
   result1=out(matchpeople)
   i=0
   while len(matchpeople)>1:
      num1=compition(matchpeople)
      result1=out(num1)
      i+=1  
   john=gambler('john')
   matchpeople=[john]
   countnum=0
   outer=[]
   winer=[]
   names=locals()#用于随机生成名字
   for i in range(119):
           names['gambler'+str(i)]=gambler('gambler'+str(i))
           matchpeople.append(names['gambler'+str(i)])
   print(j+1,result1[1],len(result1[2]),len(result1[3]))
   qq=[j+1,result1[1],len(result1[2]),len(result1[3])]
   df[j]=qq

data=pd.DataFrame(columns=['次数','完成局数','胜利','失败'])
data['次数']=df[df.index==0].values.tolist()[0]
data['完成局数']=df[df.index==1].values.tolist()[0]
data['胜利']=df[df.index==2].values.tolist()[0]
data['失败']=df[df.index==3].values.tolist()[0]
data.to_excel('gambling.xlsx')