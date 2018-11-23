

import random as ra
import pandas as pd


class gambler():
    def __init__(self,name):
        self.poker = ['a','a','a','a','b','b','b','b','c','c','c','c'] 
        self.star = 3  # 星数
        self.count = 0  # 进行局数
        self.go=ra.randint(0,1) #意愿，在0,1之间徘徊，百分之50几率行动
        self.name=name
john = gambler('john')
matchpeople=[john]
countnum=0
outer=[]
winer=[]

john.count=10
john.star=0
john.poker=['a']



names=locals()
for i in range(3):
    names['gambler'+str(i)]=gambler('gambler'+str(i))
    matchpeople.append(names['gambler'+str(i)])

gambler0.count=12
gambler0.star=3
gambler0.poker=[]

#定义match函数，用于将比赛的两个人员筛选出来,#确定参赛者
def matchg(b):
        c=b[:]   #等于b的切片，这样c变更时，不影响原来的数据
        d=ra.choice(c)  #defence 防御者
        c.remove(d)                       
        a=ra.choice(c)  #attack 攻击者
        match=[a,d]
        return match

def compition(oo):
     match=matchg(oo)
     print(match[0].name,match[1].name)
     acard=ra.choice(match[0].poker)
     dcard=ra.choice(match[1].poker)
     print('acard=',acard,'dcard=',dcard,'match0=',match[0].poker,'match1=',match[1].poker)
     match[0].poker.remove(acard)
     print('修改后0',match[0].poker,match[1].poker)
     match[1].poker.remove(dcard)
     print('修改后1',match[1].poker)
     print('acard=',acard,'dcard=',dcard,'match0=',match[0].poker,'match1=',match[1].poker)
     #a>b;b>c;c>a，定义方法，a为剪刀，b为布，c为石头
     if ((acard=='a' and dcard=='a') or (acard=='b' and dcard=='b') or (acard=='c' and dcard=='c')):
         match[0].count+=1
         match[1].count+=1
         print(match[0].name,'平局',match[1].name)
     elif ((acard=='a' and dcard=='b') or (acard=='b' and dcard=='c') or (acard=='c' and dcard=='a')):
         match[0].count+=1
         match[1].count+=1
         match[0].star+=1
         match[1].star-=1
         print(match[0].name,'赢了',match[1].name)
     elif ((acard=='a' and dcard=='c') or (acard=='b' and dcard=='a') or (acard=='c' and dcard=='b')):    
         match[0].count+=1
         match[1].count+=1
         match[0].star-=1
         match[1].star+=1
         print(match[0].name,'输给了',match[1].name)
     print(acard,match[1].name,match[1].count,match[1].star)
     print(dcard,match[0].name,match[0].count,match[0].star)
     return oo

#定义函数，输入matchpeople，输出outer，winer，新的matchpeople，每局统计数据countlist,主角信息
def out(a):
    global outer,winer,countnum
    A=0
    B=0
    C=0
    print('a的长度',len(a))
    lena=len(a)
    for i in range(len(a)):
        lenb=len(a)
        if lena>len(a):

            i-=(lena-len(a))
        print('i=',i,a[i].count,a[i].star,a[i].poker,a[i].name)
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
    countname='局数:'+str(countnum)
    return countlist,countname,winer,outer,a




result1=out(matchpeople)

print(result1[0],result1[1],result1[2],result1[3])

for i in range(20):
 num1=compition(matchpeople)
 result1=out(num1)
 print(result1[0],result1[1],result1[2],result1[3])


