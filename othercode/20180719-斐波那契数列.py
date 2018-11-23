import datetime
a=1
b=1
s=0

starttime = datetime.datetime.now()
def fbnq(x):
  global s,a,b
  if x==1:
     return 1
  elif x==2:
     return 1
  else:
     a=1
     b=1  
     for i in range(2,x):
        s=a+b
        a=b
        b=s
       # return fbnq(n-1)+fbnq(n-2) 本操作优于递归操作 
     return s
print(fbnq(1000))

endtime = datetime.datetime.now()
print(endtime - starttime)