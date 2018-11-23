import requests,re
from bs4 import BeautifulSoup



target ='http://www.msweet.com.cn/'+mixinfo[i][1]
req = requests.get(url=target)#requests获取请求
req.encoding = 'utf-8'        #定义encoding
html = req.text               #取req的属性
bf = BeautifulSoup(html,'lxml')
texts = bf.find_all('div', class_ = 'article')
bd=BeautifulSoup(str(texts),'lxml') 
text=bd.text.replace('[','').replace(']','')
re.search(r'\d\d\d\d-\d\d-\d\d',mixinfo[i][3],re.S)
with open(r'E:\gj\研究\沐甜科技\\'+mixinfo[i][0]+'_'+re.search(r'\d\d\d\d-\d\d-\d\d',mixinfo[i][3],re.S).group()+'_'+mixinfo[i][2]+".txt",'w',encoding='utf-8') as f:
               f.writelines(mixinfo[i][2]+'\n'+mixinfo[i][3]+'\n'+'\n'+text) 


